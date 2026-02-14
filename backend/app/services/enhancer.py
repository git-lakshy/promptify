from typing import Optional, Dict, List
from app.core.config import settings
from app.core.logging import logger
from app.services.llm_providers import PROVIDERS

async def enhance(
    prompt: str,
    mode: str,
    user_api_key: Optional[str] = None,
    is_byok: bool = False,
) -> Dict:
    """
    Enhance a prompt using the configured LLM providers.
    """
    errors: List[str] = []

    # BYOK Path
    if is_byok and user_api_key:
        # Detect provider based on key prefix
        if user_api_key.startswith("gsk_"):
            provider_name = "groq"
        else:
            provider_name = "gemini"
            
        call_fn = PROVIDERS.get(provider_name)
        if call_fn:
            try:
                result = await call_fn(prompt, mode, api_key=user_api_key)
                return {
                    "enhanced_prompt": result,
                    "provider_used": f"{provider_name} (BYOK)",
                    "mode": mode,
                    "error": None,
                }
            except Exception as e:
                logger.error(f"BYOK API ({provider_name}) failed: {e}")
                return {
                    "enhanced_prompt": None,
                    "provider_used": None,
                    "mode": mode,
                    "error": f"Your {provider_name} key failed: {str(e)}",
                }

    # Standard Path
    for provider_name in settings.LLM_PROVIDERS:
        call_fn = PROVIDERS.get(provider_name)
        if not call_fn:
            continue
        try:
            result = await call_fn(prompt, mode)
            return {
                "enhanced_prompt": result,
                "provider_used": provider_name,
                "mode": mode,
                "error": None,
            }
        except Exception as e:
            logger.warning(f"Provider {provider_name} failed: {e}")
            errors.append(f"{provider_name}: {str(e)}")
            continue

    logger.error(f"All providers failed. Errors: {errors}")
    return {
        "enhanced_prompt": None,
        "provider_used": None,
        "mode": mode,
        "error": f"All providers failed. Details: {'; '.join(errors)}",
    }
