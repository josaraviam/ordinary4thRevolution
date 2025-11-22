# api/rest/reports.py
# Reports + CSV export endpoints

from fastapi import APIRouter, Depends, Query
from fastapi.responses import PlainTextResponse
from typing import Optional
import io
import csv

from api.middleware.jwt_auth import get_current_user
from domain.services.vital_service import report_service


router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/summary")
async def get_summary(
    window_minutes: int = Query(5, ge=1, le=1440),
    patient_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    GET /api/reports/summary?window_minutes=5
    Get aggregated stats for time window
    Protected: requires JWT
    """
    return await report_service.get_summary(
        window_minutes=window_minutes,
        patient_id=patient_id
    )


@router.get("/export")
async def export_csv(
    window_minutes: int = Query(5, ge=1, le=1440),
    patient_id: Optional[str] = None,
    format: str = Query("csv"),
    current_user: dict = Depends(get_current_user)
):
    """
    GET /api/reports/export?window_minutes=5&format=csv
    Export readings as CSV
    Protected: requires JWT
    """
    # Get readings via service
    readings = await report_service.get_readings_for_export(
        window_minutes=window_minutes,
        patient_id=patient_id
    )

    # Build CSV
    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        "patient_id",
        "heart_rate",
        "oxygen_level",
        "body_temperature",
        "steps",
        "timestamp"
    ])

    # Rows
    for r in readings:
        writer.writerow([
            r.get("patient_id", ""),
            r.get("heart_rate", 0),
            r.get("oxygen_level", 0),
            r.get("body_temperature", 0),
            r.get("steps", 0),
            r.get("timestamp", "").isoformat() if r.get("timestamp") else ""
        ])

    csv_content = output.getvalue()

    return PlainTextResponse(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=vitals_export_{window_minutes}min.csv"
        }
    )
