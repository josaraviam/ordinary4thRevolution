from fastapi import APIRouter, Depends, Query

from api.middleware.jwt_auth import get_current_user
from domain.services.vital_service import report_service


router = APIRouter(prefix="/overview", tags=["Overview"])


@router.get("/kpis")
async def get_kpis(
    window_minutes: int = Query(5, ge=1, le=60),
    current_user: dict = Depends(get_current_user)
):
    """
    GET /api/overview/kpis?window_minutes=5
    Get dashboard KPIs
    Protected: requires JWT
    """
    return await report_service.get_kpis(window_minutes=window_minutes)
