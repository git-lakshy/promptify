from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from pydantic import BaseModel, EmailStr
from bson import ObjectId
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, decode_token, verify_password, get_password_hash
from app.core.database import get_db
from app.core.redis_client import redis_client
from app.models.user import User
from app.core.logging import logger

router = APIRouter(prefix="/api/auth", tags=["auth"])

# OAuth setup
oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# --- Request Schemas ---
class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str = ""

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False

class RefreshRequest(BaseModel):
    token: str


# --- Helper to issue tokens ---
async def _issue_tokens(user: User, remember_me: bool = False):
    """Create access/refresh tokens and store refresh in Redis."""
    access_expire = None
    if remember_me:
        from datetime import timedelta
        access_expire = timedelta(days=7)  # Longer-lived token

    access_token = create_access_token({"sub": str(user.id), "email": user.email}, expires_delta=access_expire)
    refresh_token = create_refresh_token({"sub": str(user.id)})

    # Store refresh token in Redis
    await redis_client.set(
        f"refresh_token:{user.id}",
        refresh_token,
        expire=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )
    return access_token, refresh_token


# --- Google OAuth ---
@router.get("/google/login")
async def google_login(request: Request):
    """Redirect to Google OAuth."""
    redirect_uri = f"{settings.BACKEND_URL}/api/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request, db = Depends(get_db)):
    """Handle Google OAuth callback."""
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        logger.error(f"Google OAuth error: {e}")
        raise HTTPException(status_code=400, detail="Google authentication failed")

    user_info = token.get('userinfo')
    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to get user info from Google")

    email = user_info.get('email')
    if not email:
        raise HTTPException(status_code=400, detail="Email not provided by Google")

    google_id = user_info.get('sub')
    name = user_info.get('name')
    avatar_url = user_info.get('picture')

    # Check if user exists in MongoDB
    user_doc = await db.users.find_one({"email": email})

    if not user_doc:
        user = User(
            email=email,
            name=name or "",
            avatar_url=avatar_url,
            google_id=google_id,
        )
        user_dict = user.model_dump(by_alias=True)
        if user_dict.get("_id") is None:
            user_dict.pop("_id", None)
        result = await db.users.insert_one(user_dict)
        user.id = str(result.inserted_id)
        logger.info(f"new_user_created={email}")
    else:
        user = User(**user_doc)
        # Update user info if changed
        update_data = {}
        if name and name != user.name:
            user.name = name
            update_data["name"] = name
        if avatar_url and avatar_url != user.avatar_url:
            user.avatar_url = avatar_url
            update_data["avatar_url"] = avatar_url
        
        if update_data:
            await db.users.update_one({"_id": user_doc["_id"]}, {"$set": update_data})
            # Refresh user object from database
            user_doc = await db.users.find_one({"_id": user_doc["_id"]})
            user = User(**user_doc)

    access_token, refresh_token = await _issue_tokens(user)

    # Redirect to frontend with tokens
    redirect_url = f"{settings.FRONTEND_URL}/auth/callback?token={access_token}&refresh={refresh_token}"
    return RedirectResponse(url=redirect_url)


# --- Email / Password Auth ---
@router.post("/signup")
async def signup(body: SignupRequest, db = Depends(get_db)):
    """Register a new user with email and password."""
    # Check if user exists
    existing = await db.users.find_one({"email": body.email})
    if existing:
        if existing.get("google_id") and not existing.get("password_hash"):
            raise HTTPException(
                status_code=400,
                detail="This email is registered via Google Login. Please Sign In with Google."
            )
        raise HTTPException(status_code=400, detail="Email is already registered. Please Sign In.")

    # Create user with hashed password
    user = User(
        email=body.email,
        name=body.name or body.email.split("@")[0],
        password_hash=get_password_hash(body.password),
    )
    user_dict = user.model_dump(by_alias=True)
    if user_dict.get("_id") is None:
        user_dict.pop("_id", None)
    result = await db.users.insert_one(user_dict)
    user.id = str(result.inserted_id)
    logger.info(f"new_user_signup={body.email}")

    access_token, refresh_token = await _issue_tokens(user)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
        }
    }


@router.post("/login")
async def login(body: LoginRequest, db = Depends(get_db)):
    """Authenticate with email and password."""
    user_doc = await db.users.find_one({"email": body.email})
    if not user_doc:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user_doc.get("password_hash"):
        if user_doc.get("google_id"):
            raise HTTPException(
                status_code=400,
                detail="This account is registered via Google Login. Please Sign In with Google."
            )
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user = User(**user_doc)
    if not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token, refresh_token = await _issue_tokens(user, remember_me=body.remember_me)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
        }
    }


# --- Token Refresh ---
@router.post("/refresh")
async def refresh_token(body: RefreshRequest, db = Depends(get_db)):
    """Refresh access token."""
    payload = decode_token(body.token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Check blacklist
    is_blacklisted = await redis_client.get(f"blacklist:{body.token}")
    if is_blacklisted:
        raise HTTPException(status_code=401, detail="Refresh token has been revoked")

    # Check if refresh token is valid in Redis
    stored_token = await redis_client.get(f"refresh_token:{user_id}")
    if not stored_token or stored_token != body.token:
        raise HTTPException(status_code=401, detail="Refresh token expired")

    # Get user
    try:
        user_doc = await db.users.find_one({"_id": ObjectId(user_id)})
    except Exception:
        user_doc = None

    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")

    user = User(**user_doc)

    # Create new tokens
    new_access = create_access_token({"sub": str(user.id), "email": user.email})
    new_refresh = create_refresh_token({"sub": str(user.id)})

    # Update refresh token in Redis
    await redis_client.set(
        f"refresh_token:{user.id}",
        new_refresh,
        expire=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )

    return {"access_token": new_access, "refresh_token": new_refresh, "token_type": "bearer"}


# --- Logout ---
@router.post("/logout")
async def logout(request: Request):
    """Logout user by blacklisting token."""
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        payload = decode_token(token)
        if payload:
            exp = payload.get("exp")
            if exp:
                # Blacklist token until its expiration
                ttl = max(0, exp - int(datetime.now(timezone.utc).timestamp()))
                if ttl > 0:
                    await redis_client.set(f"blacklist:{token}", "1", expire=ttl)
            # Also invalidate the refresh token in Redis
            user_id = payload.get("sub")
            if user_id:
                await redis_client.delete(f"refresh_token:{user_id}")

    return {"message": "Logged out successfully"}
