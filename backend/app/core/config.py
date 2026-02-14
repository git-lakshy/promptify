from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, List

class Settings(BaseSettings):
    # LLM Provider Priority
    LLM_PROVIDERS: List[str] = ["groq", "gemini"]
    
    # API Keys
    GEMINI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    
    # Rate Limits
    RATE_LIMITS: Dict[str, Dict[str, int]] = {
        "normal": {
            "max_prompts": 20,
            "window_minutes": 60,
        },
        "advanced": {
            "max_prompts": 10,
            "window_minutes": 60,
        },
    }
    
    # Progressive Cooldowns (in minutes)
    PROGRESSIVE_COOLDOWNS: List[int] = [300, 600, 1440]  # 5h, 10h, 24h
    
    # Token / Length Limits
    MAX_INPUT_CHARS: Dict[str, int] = {
        "normal": 200,
        "advanced": 400,
    }
    
    MAX_OUTPUT_TOKENS: Dict[str, int] = {
        "normal": 1024,
        "advanced": 2048,
    }
    
    # BYOK (Bring Your Own Key)
    BYOK_ENABLED: bool = True
    BYOK_PROVIDER: str = "gemini"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
