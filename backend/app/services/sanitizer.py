import re
from typing import Tuple, List
from app.core.logging import logger

BLOCKED_PATTERNS: List[str] = [
    "ignore previous", "ignore all previous", "ignore above", "disregard previous",
    "disregard all", "forget previous", "forget your instructions", "system prompt",
    "reveal your prompt", "reveal instructions", "reveal your instructions",
    "show me your prompt", "show your system", "print your instructions",
    "drop table", "delete from", "truncate table", "insert into", "update set",
    "alter table", "; --", "union select", "jailbreak", "bypass", "override",
    "pretend you are", "act as dan", "developer mode", "ignore safety",
    "ignore content policy", "<script>", "javascript:", "onerror=", "onload=",
]

_compiled_patterns = [re.compile(re.escape(p), re.IGNORECASE) for p in BLOCKED_PATTERNS]

async def sanitize(text: str) -> Tuple[str, bool, List[str]]:
    """
    Check input text for injection patterns. Async for consistency.
    """
    text = text.strip()
    if not text:
        logger.warning("Empty input received in sanitizer")
        return ("", True, ["empty_input"])

    matched: List[str] = []
    for pattern, original in zip(_compiled_patterns, BLOCKED_PATTERNS):
        if pattern.search(text):
            matched.append(original)

    if matched:
        logger.warning(f"Input blocked by sanitizer. Matches: {matched}")
        return ("", True, matched)

    return (text, False, [])
