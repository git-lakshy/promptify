from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import RequestValidationError
from starlette.middleware.sessions import SessionMiddleware
from app.api.router import router
from app.api.auth import router as auth_router
from app.services.rate_limiter import init_db as init_rate_limiter_db
from app.core.database import init_db as init_main_db
from app.core.logging import logger
from app.core.config import settings
from app.core.redis_client import redis_client
from app.core.middleware import MetricsMiddleware
from app.core.metrics import get_metrics
from prometheus_client import CONTENT_TYPE_LATEST


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Promptify API...")
    init_rate_limiter_db()
    await init_main_db()
    await redis_client.connect()
    yield
    # Shutdown
    logger.info("Shutting down Promptify API...")
    await redis_client.disconnect()

app = FastAPI(
    title="Promptify API",
    description="Professional AI Prompt Enhancement Engine",
    version="1.1.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session middleware (required for OAuth)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    max_age=3600,
    same_site="lax",
)

# Custom Prometheus metrics middleware
app.add_middleware(MetricsMiddleware)

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Promptify API is running",
        "version": "1.1.0",
        "docs": "/docs"
    }

# Include routers
app.include_router(router)
app.include_router(auth_router)

# Prometheus metrics endpoint - expose custom prometheus_client metrics
@app.get("/api/metrics")
async def metrics_endpoint():
    metrics_content = await get_metrics()
    # Use Response to handle bytes directly; PlainTextResponse would do str(content).encode()
    # which re-encodes bytes and corrupts the output from prometheus_client
    return Response(content=metrics_content, media_type=CONTENT_TYPE_LATEST)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation Error: {exc.errors()}")
    
    # Format list of validation errors into a single, user-friendly string
    error_messages = []
    for err in exc.errors():
        loc_path = " -> ".join([str(x) for x in err.get("loc", []) if x != "body"])
        msg = err.get("msg", "Invalid value")
        if loc_path:
            error_messages.append(f"{loc_path}: {msg}")
        else:
            error_messages.append(msg)
            
    readable_error = "; ".join(error_messages)
    return JSONResponse(
        status_code=422,
        content={"detail": readable_error},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."},
    )
