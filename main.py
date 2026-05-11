"""
Youth Organization Discovery API - Main Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

# Initialize FastAPI app
app = FastAPI(
    title="Youth Organization Discovery API",
    description="Discovers and profiles youth organizations in Stockholm",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Youth Organization Discovery API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "services": {
            "tavily": "configured" if settings.TAVILY_API_KEY else "not configured",
            "openai": "configured" if settings.OPENAI_API_KEY else "not configured",
            "firebase": "configured" if settings.FIREBASE_CREDENTIALS_PATH else "not configured"
        }
    }


# Import and include API routes
from app.api.routes import router
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
