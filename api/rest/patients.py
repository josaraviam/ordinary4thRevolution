from fastapi import APIRouter, Depends, status, Query

from api.middleware.jwt_auth import get_current_user
from domain.models.patient import PatientListResponse
from domain.models.vital import VitalDataInput, VitalListResponse
from domain.services.patient_service import patient_service
from domain.services.vital_service import vital_service
from infrastructure.pubsub.broadcaster import broadcast_vital
from config.logging_config import get_logger
from config.debug_utils import debug_timer, debug_vars, DebugContext

router = APIRouter(prefix="/patients", tags=["Patients"])
logger = get_logger("api.patients")


@router.post("/data", status_code=status.HTTP_201_CREATED)
@debug_timer
async def ingest_patient_data(
    data: VitalDataInput,
    current_user: dict = Depends(get_current_user)
):
    """
    POST /api/patients/data
    Receive new vital readings from Node-RED
    Protected: requires JWT
    """
    logger.info("Ingesting patient vital data", extra={
        "patient_id": data.deviceId,
        "user_id": current_user.get("id"),
        "operation": "ingest_vital_data"
    })
    
    debug_vars(
        patient_id=data.deviceId,
        heart_rate=data.heartRate,
        oxygen_level=data.oxygenLevel,
        body_temperature=data.bodyTemperature,
        steps=data.steps
    )
    
    with DebugContext("vital_data_processing"):
        # Use service layer to handle all logic
        result = await vital_service.ingest_vital_data(data)

        # Broadcast for GraphQL subscriptions
        await broadcast_vital(
            patient_id=data.deviceId,
            heart_rate=data.heartRate,
            oxygen_level=data.oxygenLevel,
            body_temperature=data.bodyTemperature,
            steps=data.steps,
            timestamp=data.timestamp
        )
    
    logger.info("Patient vital data ingested successfully", extra={
        "patient_id": result["patient_id"],
        "patient_status": result["patient_status"],
        "operation": "ingest_vital_data"
    })

    return {
        "status": "ok",
        "message": "Vital data ingested",
        "patient_id": result["patient_id"],
        "patient_status": result["patient_status"]
    }


@router.get("", response_model=PatientListResponse)
async def list_patients(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """
    GET /api/patients
    List all patients with latest metrics
    Protected: requires JWT
    """
    return await patient_service.get_all_patients(page=page, page_size=page_size)


@router.get("/{patient_id}/readings", response_model=VitalListResponse)
async def get_patient_readings(
    patient_id: str,
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """
    GET /api/patients/{patient_id}/readings
    Get recent readings for a patient
    Protected: requires JWT
    """
    return await vital_service.get_patient_readings(patient_id, limit=limit)
