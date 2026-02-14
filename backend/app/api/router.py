from fastapi import APIRouter, Request, HTTPException, Depends
from typing import Annotated
from app.models.schemas import EnhanceRequest, EnhanceResponse, StatsResponse
from app.services.sanitizer import sanitize
from app.services.rate_limiter import check_rate_limit, record_usage, get_usage_stats, compute_fingerprint
from app.services.enhancer import enhance
from app.core.config import settings
from app.core.logging import logger

router = APIRouter(prefix="/api")

def get_fingerprint(request: Request, client_fp: str) -> str:
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "")
    lang = request.headers.get("accept-language", "")
    return compute_fingerprint(ip, ua, lang, client_fp)

@router.post("/enhance", response_model=EnhanceResponse)
async def enhance_prompt(body: EnhanceRequest, request: Request):
    fingerprint = get_fingerprint(request, body.fingerprint)
    is_byok = bool(body.user_api_key and settings.BYOK_ENABLED)

    # Rate limit check (skip if BYOK)
    if not is_byok:
        allowed, message, retry_after = await check_rate_limit(fingerprint, body.mode)
        if not allowed:
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

    # Sanitize input
    clean_text, is_blocked, matched = await sanitize(body.prompt)
    if is_blocked:
        return EnhanceResponse(
            mode=body.mode,
            blocked=True,
            blocked_keywords=matched,
            error="Restricted patterns detected. Please rephrase.",
        )

    # Enhance via LLM
    result = await enhance(
        prompt=clean_text,
        mode=body.mode,
        user_api_key=body.user_api_key if is_byok else None,
        is_byok=is_byok,
    )

    # Record usage
    if not is_byok and not result["error"]:
        await record_usage(fingerprint, body.mode)

    usage = await get_usage_stats(fingerprint, body.mode)

    return EnhanceResponse(
        enhanced_prompt=result["enhanced_prompt"],
        provider_used=result["provider_used"],
        mode=body.mode,
        usage=usage,
        error=result["error"]
    )

@router.get("/stats", response_model=StatsResponse)
async def get_stats(request: Request, fingerprint: str = ""):
    fp = get_fingerprint(request, fingerprint)
    return StatsResponse(
        normal=await get_usage_stats(fp, "normal"),
        advanced=await get_usage_stats(fp, "advanced"),
    )

@router.get("/health")
async def health():
    return {"status": "ok", "service": "promptify"}
