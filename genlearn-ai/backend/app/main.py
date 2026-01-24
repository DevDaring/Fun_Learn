"""
Fun Learn - Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.config import settings
from app.api.routes import (
    auth,
    users,
    learning,
    avatar,
    characters,
    quiz,
    voice,
    video,
    tournaments,
    teams,
    admin,
    chat,
    features,
    feynman
)
from app.services.provider_factory import ProviderFactory


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    # Startup
    print("=" * 60)
    print("🚀 Starting Fun Learn...")
    print("=" * 60)
    print(f"📦 AI Provider: {os.getenv('AI_PROVIDER', 'gemini')}")
    print(f"🖼️  Image Provider: {os.getenv('IMAGE_PROVIDER', 'fibo')}")
    print(f"🔊 TTS Provider: {os.getenv('VOICE_TTS_PROVIDER', 'gcp')}")
    print(f"🎤 STT Provider: {os.getenv('VOICE_STT_PROVIDER', 'gcp')}")
    print("-" * 60)

    # Check provider health
    try:
        print("Checking provider health...")
        status = await ProviderFactory.check_all_providers()
        for name, info in status.items():
            if info["status"] == "healthy":
                print(f"  ✅ {name}: {info['provider']} - {info['status']}")
            else:
                print(f"  ❌ {name}: {info['provider']} - {info['status']}")
                if "error" in info:
                    print(f"     Error: {info['error']}")
    except Exception as e:
        print(f"  ⚠️  Provider health check failed: {e}")

    print("=" * 60)
    print("✨ Fun Learn is ready!")
    print(f"📚 API Documentation: http://{settings.BACKEND_HOST}:{settings.BACKEND_PORT}/docs")
    print("=" * 60)

    yield

    # Shutdown
    print("\n" + "=" * 60)
    print("👋 Shutting down Fun Learn...")
    print("=" * 60)


app = FastAPI(
    title="Fun Learn",
    description="Generative AI-Enabled Adaptive Learning System",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://[::1]:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for media
if settings.MEDIA_DIR.exists():
    app.mount("/media", StaticFiles(directory=str(settings.MEDIA_DIR)), name="media")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(learning.router, prefix="/api/learning", tags=["Learning"])
app.include_router(avatar.router, prefix="/api/avatar", tags=["Avatar"])
app.include_router(characters.router, prefix="/api/characters", tags=["Characters"])
app.include_router(quiz.router, prefix="/api/quiz", tags=["Quiz"])
app.include_router(voice.router, prefix="/api/voice", tags=["Voice"])
app.include_router(video.router, prefix="/api/video", tags=["Video"])
app.include_router(tournaments.router, prefix="/api/tournaments", tags=["Tournaments"])
app.include_router(teams.router, prefix="/api/teams", tags=["Teams"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(features.router, prefix="/api/features", tags=["Enhanced Features"])
app.include_router(feynman.router, prefix="/api")  # Feynman Engine


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Fun Learn",
        "version": "1.0.0-prototype",
        "description": "Generative AI-Enabled Adaptive Learning System",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint

    Returns system status and provider health
    """
    try:
        providers = await ProviderFactory.check_all_providers()
        all_healthy = all(p["status"] == "healthy" for p in providers.values())

        return {
            "status": "healthy" if all_healthy else "degraded",
            "providers": providers,
            "version": "1.0.0-prototype"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "version": "1.0.0-prototype"
        }
