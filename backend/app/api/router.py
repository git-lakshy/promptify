import time
from fastapi import APIRouter, Request, HTTPException, Depends
from typing import Optional
from datetime import datetime, timezone
from bson import ObjectId
from app.models.schemas import EnhanceRequest, EnhanceResponse, StatsResponse
from app.services.sanitizer import sanitize
from app.services.rate_limiter import check_rate_limit, record_usage, get_usage_stats
from app.services.enhancer import enhance
from app.services.cache import get_cached_response, set_cached_response
from app.core.config import settings
from app.core.logging import logger
from app.core.database import get_db
from app.core.security import decode_token
from app.core.redis_client import redis_client
from app.core.metrics import llm_calls_total, llm_latency, rate_limit_hits, active_users_gauge
from app.models.user import User

router = APIRouter(prefix="/api")

async def get_current_user(request: Request, db = Depends(get_db)) -> Optional[User]:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ")[1]
    payload = decode_token(token)
    if not payload:
        return None

    # Check blacklist
    is_blacklisted = await redis_client.get(f"blacklist:{token}")
    if is_blacklisted:
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    try:
        user_doc = await db.users.find_one({"_id": ObjectId(user_id)})
        if user_doc:
            return User(**user_doc)
    except Exception:
        pass
    return None

@router.post("/enhance", response_model=EnhanceResponse)
async def enhance_prompt(
    body: EnhanceRequest,
    request: Request,
    db = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    user_id = current_user.id if current_user else None
    fingerprint = str(current_user.id) if current_user else request.headers.get("x-fingerprint", "anonymous")

    is_byok = bool(body.user_api_key and settings.BYOK_ENABLED)

    # Rate limit check
    if not is_byok:
        allowed, message, retry_after = await check_rate_limit(fingerprint, body.mode)
        if not allowed:
            rate_limit_hits.labels(mode=body.mode, user_type="logged_in" if current_user else "anonymous").inc()
            usage = await get_usage_stats(fingerprint, body.mode)
            return EnhanceResponse(
                mode=body.mode,
                rate_limited=True,
                rate_limit_message=message,
                retry_after=retry_after,
                usage=usage,
            )

    # Input length check
    max_chars = settings.MAX_INPUT_CHARS.get(body.mode, 2000)
    if len(body.prompt) > max_chars:
        return EnhanceResponse(
            mode=body.mode,
            error=f"Input too long. Max {max_chars} chars for {body.mode} mode.",
        )

    # Check cache first
    if not is_byok:
        cached = await get_cached_response(body.prompt, body.mode)
        if cached:
            return EnhanceResponse(
                enhanced_prompt=cached,
                provider_used="cache",
                mode=body.mode,
                usage=await get_usage_stats(fingerprint, body.mode),
            )

    # Sanitize input
    clean_text, is_blocked, matched, easter_egg = await sanitize(body.prompt)
    if is_blocked:
        return EnhanceResponse(
            mode=body.mode,
            blocked=True,
            blocked_keywords=matched,
            error=easter_egg,
        )

    # Track active users
    if current_user:
        active_users_gauge.inc()

    start_time = time.perf_counter()
    try:
        # Enhance via LLM
        result = await enhance(
            prompt=clean_text,
            mode=body.mode,
            user_api_key=body.user_api_key if is_byok else None,
            is_byok=is_byok,
        )
    finally:
        if current_user:
            active_users_gauge.dec()

    latency = time.perf_counter() - start_time

    # Record metrics
    provider = result.get("provider_used") or "unknown"
    status = "error" if result.get("error") else "success"
    llm_calls_total.labels(provider=provider, mode=body.mode, status=status).inc()
    if not result.get("error"):
        llm_latency.labels(provider=provider, mode=body.mode).observe(latency)

    # Cache the response
    if not is_byok and not result.get("error"):
        await set_cached_response(body.prompt, body.mode, result["enhanced_prompt"])
        # Record usage in rate-limiter DB
        await record_usage(fingerprint, body.mode)

    usage = await get_usage_stats(fingerprint, body.mode)

    # Log to main database (MongoDB)
    if not is_byok:
        usage_log = {
            "user_id": user_id,
            "fingerprint": fingerprint,
            "mode": body.mode,
            "provider_used": provider,
            "latency_ms": round(latency * 1000, 2),
            "timestamp": datetime.now(timezone.utc)
        }
        await db.usage_logs.insert_one(usage_log)

        if current_user:
            prompt_history = {
                "user_id": user_id,
                "original_prompt": body.prompt,
                "enhanced_prompt": result.get("enhanced_prompt"),
                "mode": body.mode,
                "provider_used": result.get("provider_used"),
                "created_at": datetime.now(timezone.utc)
            }
            await db.prompt_histories.insert_one(prompt_history)

    return EnhanceResponse(
        enhanced_prompt=result["enhanced_prompt"],
        provider_used=result["provider_used"],
        mode=body.mode,
        usage=usage,
        error=result["error"],
    )

@router.get("/stats", response_model=StatsResponse)
async def get_stats(request: Request):
    fingerprint = request.headers.get("x-fingerprint", "anonymous")
    return StatsResponse(
        normal=await get_usage_stats(fingerprint, "normal"),
        advanced=await get_usage_stats(fingerprint, "advanced"),
    )

@router.get("/health")
async def health():
    return {"status": "ok", "service": "promptify"}

@router.get("/me")
async def me(current_user: Optional[User] = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "avatar_url": current_user.avatar_url,
        "tier": current_user.tier,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
    }
