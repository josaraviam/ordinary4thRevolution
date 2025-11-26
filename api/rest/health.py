from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """
    GET /api/health
    Basic health check // no auth required
    """
    return {
        "status": "ok",
        "service": "Smart Health Monitoring API",
        "version": "1.0.0"
    }
