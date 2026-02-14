import google.generativeai as genai
import httpx
import time
from groq import AsyncGroq
from typing import Optional, Dict
from app.core.config import settings
from app.core.logging import logger
from app.services.system_prompts import NORMAL_SYSTEM_PROMPT, ADVANCED_SYSTEM_PROMPT

def get_system_prompt(mode: str) -> str:
    return ADVANCED_SYSTEM_PROMPT if mode == "advanced" else NORMAL_SYSTEM_PROMPT

async def call_gemini(prompt: str, mode: str, api_key: Optional[str] = None) -> str:
    key = api_key or settings.GEMINI_API_KEY
    if not key:
        raise ValueError("Gemini API key not configured")

    genai.configure(api_key=key)
    # Using models/ prefix to ensure correctness
    model = genai.GenerativeModel(
        model_name="models/gemini-3-flash-preview",
        system_instruction=get_system_prompt(mode),
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=settings.MAX_OUTPUT_TOKENS.get(mode, 1024),
            temperature=0.7,
        ),
    )
    duration_perf = 0
    start_time = time.perf_counter()
    response = await model.generate_content_async(prompt)
    duration_perf = time.perf_counter() - start_time
    logger.info(f"Gemini call took {duration_perf:.2f}s")
    return response.text

async def call_groq(prompt: str, mode: str, api_key: Optional[str] = None) -> str:
    key = api_key or settings.GROQ_API_KEY
    if not key:
        raise ValueError("Groq API key not configured")

    client = AsyncGroq(api_key=key)
    
    # Using Llama 3.3 70B via Groq
    start_time = time.perf_counter()
    chat_completion = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": get_system_prompt(mode)},
            {"role": "user", "content": prompt},
        ],
        model="llama-3.3-70b-versatile",
        max_tokens=settings.MAX_OUTPUT_TOKENS.get(mode, 1024),
        temperature=0.7,
    )
    duration_perf = time.perf_counter() - start_time
    logger.info(f"Groq call took {duration_perf:.2f}s")
    return chat_completion.choices[0].message.content

PROVIDERS = {
    "gemini": call_gemini,
    "groq": call_groq,
}
