from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import games_router, recommendations_router, auth_router
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Steam Backlog Tracker API",
    description="AI-powered game recommendation system for Steam libraries",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
        "http://localhost:3000",  # Next.js dev server
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(games_router)
app.include_router(recommendations_router)

@app.get("/")
async def root():
    """
    Root endpoint - API health check
    """
    return {
        "message": "Steam Backlog Tracker API",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "steam_api_configured": bool(settings.steam_api_key)
    }

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Steam Backlog Tracker API...")
    logger.info(f"Frontend URL: {settings.frontend_url}")
    logger.info(f"Backend URL: {settings.backend_url}")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on code changes (dev only)
    )
