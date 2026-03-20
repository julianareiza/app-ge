import os

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    return {"status": "healthy"}


@router.get("/ready")
async def ready():
    return {"status": "ready"}


@router.get("/version")
async def version():
    return {
        "version": os.getenv("APP_VERSION", "unknown"),
        "commit": os.getenv("APP_COMMIT", "unknown"),
    }
