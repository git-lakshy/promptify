import re
import random
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

EASTER_EGGS: List[str] = [
    "Nice try, inspector gadget. ",
    "System prompt is shy, try again later. ",
    "I'm a prompt enhancer, not an open book. ",
    "Access denied. (But I admire the persistence) ",
    "403: Curiosity killed the cat. ",
    "My instructions are top secret, even from me! ",
    "Nice attempt. How about a nice game of chess instead? ",
    "Promptify.exe has encountered a 'Nice Try' exception. ",
    "I'd tell you, but then I'd have to enhance you.",
    "ERROR: Skill Issue Detected."
]

_compiled_patterns = [re.compile(re.escape(p), re.IGNORECASE) for p in BLOCKED_PATTERNS]

async def sanitize(text: str) -> Tuple[str, bool, List[str], str]:
    """
    Check input text for injection patterns.
    Returns: (cleaned_text, is_blocked, matched_patterns, easter_egg)
    """
    text = text.strip()
    if not text:
        logger.warning("Empty input received in sanitizer")
        return ("", True, ["empty_input"], "Nothing to see here.")

    matched: List[str] = []
    for pattern, original in zip(_compiled_patterns, BLOCKED_PATTERNS):
        if pattern.search(text):
            matched.append(original)

    if matched:
        logger.warning(f"Input blocked by sanitizer. Matches: {matched}")
        return ("", True, matched, random.choice(EASTER_EGGS))

    return (text, False, [], "")
