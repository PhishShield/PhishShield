from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from utils.rate_limiter import limiter

from database import init_database

from routes.scan import router as scan_router
from routes.history import router as history_router
from routes.health import router as health_router


# =========================================================
# Database Initialization
# =========================================================

init_database()


# =========================================================
# Rate Limiter
# =========================================================

limiter = Limiter(key_func=get_remote_address)


# =========================================================
# FastAPI Application
# =========================================================

app = FastAPI(
    title="PhishShield API",
    description="Backend API for phishing URL detection",
    version="1.0.0"
)


# Register rate-limit exception handler
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)


# =========================================================
# CORS Configuration
# =========================================================

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# Register API Routes
# =========================================================

app.include_router(scan_router)
app.include_router(history_router)
app.include_router(health_router)


# =========================================================
# Home Endpoint
# =========================================================

@app.get("/")
async def home():
    return {
        "message": "Welcome to PhishShield API",
        "status": "Running",
        "version": "1.0.0"
    }


# =========================================================
# About Endpoint
# =========================================================

@app.get("/about")
async def about():
    return {
        "project": "PhishShield",
        "description": "AI-powered phishing detection system",
        "developer": "Backend Team"
    }


# =========================================================
# API Health / Status
# =========================================================

@app.get("/status")
@limiter.limit("30/minute")
async def status(request: Request):
    return {
        "status": "online",
        "service": "PhishShield API"
    }
