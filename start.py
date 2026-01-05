#!/usr/bin/env python3
"""
Startup script for Railway deployment
"""
import os
import sys
import time
from app.config import settings

def wait_for_database():
    """Wait for database to be ready"""
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            from app.database import engine
            # Try to connect to database
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            print("✅ Database connection successful")
            return True
        except Exception as e:
            retry_count += 1
            print(f"⚠️ Database connection attempt {retry_count}/{max_retries} failed: {e}")
            if retry_count < max_retries:
                time.sleep(2)
            else:
                print("❌ Database connection failed after all retries")
                return False
    
    return False

def create_tables():
    """Create database tables"""
    try:
        from app.database import engine, Base
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create database tables: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    try:
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        os.makedirs(settings.QR_CODE_DIR, exist_ok=True)
        print(f"✅ Directories created: {settings.UPLOAD_DIR}, {settings.QR_CODE_DIR}")
        return True
    except Exception as e:
        print(f"❌ Failed to create directories: {e}")
        return False

def start_app():
    """Start the FastAPI application"""
    import uvicorn
    
    print("🚀 Starting Devcon '26 API...")
    print(f"   Environment: {settings.ENVIRONMENT}")
    print(f"   Port: {settings.PORT}")
    print(f"   Debug: {settings.DEBUG}")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        workers=1,
        reload=False,
        access_log=True
    )

def main():
    """Main startup function"""
    print("🔄 Initializing Devcon '26 API...")
    
    # Step 1: Create directories
    if not create_directories():
        print("⚠️ Directory creation failed, but continuing...")
    
    # Step 2: Wait for database
    if not wait_for_database():
        print("❌ Database not ready, but starting app anyway...")
    
    # Step 3: Create tables
    if not create_tables():
        print("⚠️ Table creation failed, but continuing...")
    
    # Step 4: Start the app
    start_app()

if __name__ == "__main__":
    main()