# api/rest/alerts.py
# Alert management endpoints

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional

from api.middleware.jwt_auth import get_current_user
from domain.models.vital import AlertListResponse
from domain.services.vital_service import alert_service
from domain.exceptions.custom_exceptions import (
    AlertNotFoundError,
    AlertAlreadyAcknowledgedError,
)


router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("", response_model=AlertListResponse)
async def list_alerts(
    status_filter: Optional[str] = Query(None, alias="status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """
    GET /api/alerts?status=ACTIVE
    List alerts // filter by status
    Protected: requires JWT
    """
    return await alert_service.get_alerts(
        status_filter=status_filter,
        skip=skip,
        limit=limit
    )


@router.post("/{alert_id}/ack")
async def acknowledge_alert(
    alert_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    POST /api/alerts/{alert_id}/ack
    Acknowledge an active alert
    Protected: requires JWT
    """
    try:
        result = await alert_service.acknowledge_alert(alert_id)
        return {
            "status": "ok",
            "message": f"Alert {alert_id} acknowledged",
            "alert_id": result["alert_id"]
        }
    except AlertNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )
    except AlertAlreadyAcknowledgedError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
