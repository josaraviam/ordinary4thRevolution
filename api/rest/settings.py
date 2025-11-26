from fastapi import APIRouter, Depends, HTTPException, status

from api.middleware.jwt_auth import get_current_user
from domain.models.vital import ThresholdSettings
from domain.services.vital_service import vital_service


router = APIRouter(prefix="/settings", tags=["Settings"])


@router.get("/thresholds", response_model=ThresholdSettings)
async def get_thresholds(
    current_user: dict = Depends(get_current_user)
):
    """
    GET /api/settings/thresholds
    Get current alert thresholds
    Protected: requires JWT
    """
    return await vital_service.get_thresholds()


@router.put("/thresholds", response_model=ThresholdSettings)
async def update_thresholds(
    thresholds: ThresholdSettings,
    current_user: dict = Depends(get_current_user)
):
    """
    PUT /api/settings/thresholds
    Update alert thresholds
    Protected: requires JWT
    """
    success = await vital_service.update_thresholds(thresholds)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update thresholds"
        )

    return thresholds
