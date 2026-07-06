from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, List
import os

class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = "development"

    # LLM Provider Priority
    LLM_PROVIDERS: List[str] = ["groq", "gemini"]

    # API Keys
    GEMINI_API_KEY: str = ""
    GROQ_API_KEY: str = ""

    # Database
    DATABASE_URL: str = "mongodb://localhost:27017/promptify"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Auth
    SECRET_KEY: str = "supersecretkeychangeme"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    FRONTEND_URL: str = "http://localhost:5173"
    BACKEND_URL: str = "http://localhost:8000"

    # Rate Limits
    RATE_LIMITS: Dict[str, Dict[str, int]] = {
        "normal": {
            "max_hourly": 10,
            "max_daily": 20,
        },
        "advanced": {
            "max_hourly": 5,
            "max_daily": 10,
        },
    }

    # Progressive Cooldowns (in minutes)
    PROGRESSIVE_COOLDOWNS: List[int] = [300, 600, 1440]

    # Token / Length Limits
    MAX_INPUT_CHARS: Dict[str, int] = {
        "normal": 200,
        "advanced": 400,
    }

    MAX_OUTPUT_TOKENS: Dict[str, int] = {
        "normal": 1024,
        "advanced": 2048,
    }

    # CORS (comma-separated list for production)
    ALLOWED_ORIGINS: List[str] = [
        origin.strip()
        for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",")
        if origin.strip()
    ]

    # BYOK (Bring Your Own Key)
    BYOK_ENABLED: bool = True
    BYOK_PROVIDER: str = "gemini"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
