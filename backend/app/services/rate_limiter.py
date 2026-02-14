import hashlib
import sqlite3
import time
from datetime import datetime, timezone
from typing import Tuple, Optional, Dict
from app.core.config import settings
from app.core.logging import logger

DB_PATH = "rate_limiter.db"

def init_db():
    """Initialize the SQLite database."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS usage_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fingerprint TEXT NOT NULL,
                mode TEXT NOT NULL,
                timestamp REAL NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_fp_mode ON usage_log(fingerprint, mode);

            CREATE TABLE IF NOT EXISTS cooldowns (
                fingerprint TEXT PRIMARY KEY,
                strike_count INTEGER DEFAULT 0,
                cooldown_until REAL DEFAULT 0,
                last_strike_date TEXT DEFAULT ''
            );
        """)
        conn.commit()

def compute_fingerprint(ip: str, user_agent: str, accept_lang: str, client_fp: str) -> str:
    raw = f"{ip}|{user_agent}|{accept_lang}|{client_fp}"
    return hashlib.sha256(raw.encode()).hexdigest()[:32]

def _today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

async def check_rate_limit(fingerprint: str, mode: str) -> Tuple[bool, Optional[str], Optional[int]]:
    now = time.time()
    today = _today_str()

    with sqlite3.connect(DB_PATH) as conn:
        # Check cooldown
        cursor = conn.execute(
            "SELECT strike_count, cooldown_until, last_strike_date FROM cooldowns WHERE fingerprint = ?",
            (fingerprint,)
        )
        row = cursor.fetchone()
        strike_count, cooldown_until, last_strike_date = (row[0], row[1], row[2]) if row else (0, 0.0, "")

        if last_strike_date and last_strike_date != today:
            conn.execute(
                "UPDATE cooldowns SET strike_count = 0, cooldown_until = 0, last_strike_date = ? WHERE fingerprint = ?",
                (today, fingerprint)
            )
            conn.commit()
            strike_count, cooldown_until = 0, 0.0

        if cooldown_until > now:
            remaining = int(cooldown_until - now)
            time_str = f"{remaining // 3600}h {(remaining % 3600) // 60}m" if remaining >= 3600 else f"{remaining // 60}m"
            return False, f"Temporarily rate-limited. Try again in {time_str}, or use BYOK.", remaining

        # Check rolling windows
        limits = settings.RATE_LIMITS.get(mode, settings.RATE_LIMITS["normal"])
        
        # 1. Hourly Check (60 mins)
        hour_start = now - 3600
        cursor = conn.execute(
            "SELECT COUNT(*) FROM usage_log WHERE fingerprint = ? AND mode = ? AND timestamp > ?",
            (fingerprint, mode, hour_start)
        )
        hour_count = cursor.fetchone()[0]

        # 2. Daily Check (24 hours)
        day_start = now - 86400
        cursor = conn.execute(
            "SELECT COUNT(*) FROM usage_log WHERE fingerprint = ? AND mode = ? AND timestamp > ?",
            (fingerprint, mode, day_start)
        )
        day_count = cursor.fetchone()[0]

        if hour_count >= limits["max_hourly"] or day_count >= limits["max_daily"]:
            cooldown_idx = min(strike_count, len(settings.PROGRESSIVE_COOLDOWNS) - 1)
            cooldown_minutes = settings.PROGRESSIVE_COOLDOWNS[cooldown_idx]
            cooldown_until_ts = now + (cooldown_minutes * 60)

            conn.execute("""
                INSERT INTO cooldowns (fingerprint, strike_count, cooldown_until, last_strike_date)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(fingerprint) DO UPDATE SET
                    strike_count = strike_count + 1,
                    cooldown_until = ?,
                    last_strike_date = ?
            """, (fingerprint, strike_count + 1, cooldown_until_ts, today, cooldown_until_ts, today))
            conn.commit()

            msg = "Daily limit reached." if day_count >= limits["max_daily"] else "Hourly limit reached."
            return False, f"{msg} Locked for {cooldown_minutes // 60} hours. Use BYOK or wait.", cooldown_minutes * 60

    return True, None, None

async def record_usage(fingerprint: str, mode: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO usage_log (fingerprint, mode, timestamp) VALUES (?, ?, ?)",
            (fingerprint, mode, time.time())
        )
        conn.commit()

async def get_usage_stats(fingerprint: str, mode: str) -> Dict:
    now = time.time()
    limits = settings.RATE_LIMITS.get(mode, settings.RATE_LIMITS["normal"])
    hour_start = now - 3600
    day_start = now - 86400

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "SELECT COUNT(*) FROM usage_log WHERE fingerprint = ? AND mode = ? AND timestamp > ?",
            (fingerprint, mode, hour_start)
        )
        hour_count = cursor.fetchone()[0]
        
        cursor = conn.execute(
            "SELECT COUNT(*) FROM usage_log WHERE fingerprint = ? AND mode = ? AND timestamp > ?",
            (fingerprint, mode, day_start)
        )
        day_count = cursor.fetchone()[0]

        cursor = conn.execute("SELECT strike_count, cooldown_until FROM cooldowns WHERE fingerprint = ?", (fingerprint,))
        row = cursor.fetchone()
        strike_count, cooldown_until = row if row else (0, 0.0)

    return {
        "used_hourly": hour_count,
        "used_daily": day_count,
        "limit_hourly": limits["max_hourly"],
        "limit_daily": limits["max_daily"],
        "is_cooling_down": cooldown_until > now,
        "cooldown_remaining": max(0, int(cooldown_until - now)) if cooldown_until > now else 0,
        "strike_count": strike_count,
    }
