"""
Main FastAPI application.
Initializes app, configures middleware, and registers routes.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys
from config import get_settings
from database import init_db
from auth.routes import router as auth_router
from analysis.routes import router as analysis_router

# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO"
)
try:
    logger.add(
        "logs/app.log",
        rotation="500 MB",
        retention="10 days",
        level="DEBUG"
    )
except OSError:
    # Likely running in a read-only environment (e.g., Vercel)
    logger.warning("File logging disabled: Read-only file system detected.")

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="Hybrid-Analyzer API",
    description="AI-powered text analysis using Hugging Face and Gemini",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    root_path="/api"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth_router)
app.include_router(analysis_router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    logger.info("Starting Hybrid-Analyzer API")
    logger.info("Initializing database...")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        # We don't raise here so the app can still start and return health checks/logs


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Hybrid-Analyzer API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Hybrid-Analyzer API"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
