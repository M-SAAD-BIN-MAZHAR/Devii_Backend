from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from app.api.v1.api import api_router
from app.config import settings
import os
 
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.QR_CODE_DIR, exist_ok=True)

app = FastAPI(
    title="Devcon '26 API",
    description="Backend API for Devcon '26 Technical Event",
    version="1.0.0"
)

 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

 
app.mount("/static", StaticFiles(directory="app/static"), name="static")

 
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Devcon '26 API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

 
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred"}
    )