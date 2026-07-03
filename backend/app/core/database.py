from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
from app.core.config import settings
from app.core.logging import logger

# Build async database URL
db_url = settings.DATABASE_URL
if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Create async engine
engine = create_async_engine(
    db_url,
    echo=settings.ENVIRONMENT == "development",
    future=True,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for models
Base = declarative_base()

async def get_db():
    """Dependency to get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def _run_migrations(conn):
    """Run any pending database migrations."""
    try:
        # Try to add password_hash column (PostgreSQL syntax with IF NOT EXISTS)
        await conn.execute(text(
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255)"
        ))
        logger.info("Migration applied: ensured password_hash column exists")
    except Exception as e:
        # For SQLite or if column already exists
        logger.debug(f"Migration check: {e}")
        try:
            await conn.execute(text(
                "ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)"
            ))
            logger.info("Migration applied: added password_hash column")
        except Exception:
            # Column already exists or other issue, safe to ignore
            pass

async def init_db():
    """Initialize database - create tables and run migrations."""
    from app.models.user import User
    from app.models.usage import UsageLog
    from app.models.prompt_history import PromptHistory

    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(Base.metadata.create_all)
        # Run migrations
        await _run_migrations(conn)

    logger.info("Database initialized")
