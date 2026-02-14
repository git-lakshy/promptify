from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class EnhanceRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=5000)
    mode: str = Field(default="normal", pattern="^(normal|advanced)$")
    fingerprint: str = Field(default="", max_length=50000)
    user_api_key: Optional[str] = Field(
        default=None,
        description="Optional: your own Gemini API key (never stored, used once and discarded)",
    )

class EnhanceResponse(BaseModel):
    enhanced_prompt: Optional[str] = None
    provider_used: Optional[str] = None
    mode: str = "normal"
    blocked: bool = False
    blocked_keywords: List[str] = []
    rate_limited: bool = False
    rate_limit_message: Optional[str] = None
    retry_after: Optional[int] = None
    error: Optional[str] = None
    usage: Optional[Dict] = None

class StatsResponse(BaseModel):
    normal: Dict
    advanced: Dict
