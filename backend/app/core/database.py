from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.core.logging import logger

class MongoDBConnection:
    client: AsyncIOMotorClient = None
    db = None

db_connection = MongoDBConnection()

async def init_db():
    """Initialize MongoDB connection and build collections and indexes."""
    logger.info("Initializing MongoDB connection...")
    
    # Initialize client
    db_connection.client = AsyncIOMotorClient(settings.DATABASE_URL)
    
    # Try parsing db name from connection string (e.g. mongodb://host/db_name)
    # If not found or fallback, default to "promptify"
    db_name = "promptify"
    try:
        # Split string by / and extract database part before query params
        path_parts = settings.DATABASE_URL.split("/")
        if len(path_parts) > 3:
            db_part = path_parts[3].split("?")[0]
            if db_part:
                db_name = db_part
    except Exception as e:
        logger.warning(f"Could not parse database name from URL, using default: {e}")
        
    db_connection.db = db_connection.client[db_name]
    
    # Create indexes asynchronously
    try:
        # Users indexes
        await db_connection.db.users.create_index("email", unique=True)
        await db_connection.db.users.create_index("google_id", unique=True, sparse=True)
        
        # Usage logs indexes
        await db_connection.db.usage_logs.create_index([("fingerprint", 1), ("mode", 1)])
        await db_connection.db.usage_logs.create_index("timestamp")
        
        # Prompt history indexes
        await db_connection.db.prompt_histories.create_index("user_id")
        await db_connection.db.prompt_histories.create_index("created_at")
        
        logger.info("MongoDB connection initialized and indexes verified/created successfully.")
    except Exception as e:
        logger.error(f"Error creating MongoDB indexes: {e}")
        raise e

async def get_db():
    """Dependency to retrieve MongoDB database instance."""
    return db_connection.db
