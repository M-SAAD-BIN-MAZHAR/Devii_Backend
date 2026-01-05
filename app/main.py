from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime
from app.api.v1.api import api_router
from app.config import settings
from app.database import engine, Base

# Create database tables (with error handling)
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
except Exception as e:
    print(f"⚠️ Database table creation failed: {e}")
    # Continue anyway - tables might already exist

# Create FastAPI app
app = FastAPI(
    title="Devcon '26 Registration System API",
    description="Backend API for Devcon '26 Registration System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for Railway deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directories if they don't exist (with error handling)
try:
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.QR_CODE_DIR, exist_ok=True)
    print(f"✅ Upload directories created: {settings.UPLOAD_DIR}, {settings.QR_CODE_DIR}")
except Exception as e:
    print(f"⚠️ Directory creation failed: {e}")
    # Continue anyway

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Devcon '26 Registration API",
        "status": "operational",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }

@app.get("/health")
async def health_check():
    try:
        # Basic health check without database dependency
        return {
            "status": "healthy", 
            "environment": settings.ENVIRONMENT,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.DEBUG
    )