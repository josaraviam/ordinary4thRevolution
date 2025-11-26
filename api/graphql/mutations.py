import strawberry
from datetime import datetime

from api.graphql.types import (
    ThresholdType, ThresholdInput,
    VitalDataInput, IngestResponse, AckResponse
)
from domain.models.vital import VitalDataInput as VitalDataInputModel, ThresholdSettings
from domain.services.vital_service import vital_service, alert_service
from domain.exceptions.custom_exceptions import (
    AlertNotFoundError,
    AlertAlreadyAcknowledgedError,
)
from infrastructure.pubsub.broadcaster import broadcast_vital


@strawberry.type
class Mutation:
    """Root GraphQL mutations"""

    @strawberry.mutation
    async def ingest_vital_data(self, data: VitalDataInput) -> IngestResponse:
        """
        Ingest vital data from device/simulation
        Similar to POST /api/patients/data
        """
        # Convert to domain model
        vital_input = VitalDataInputModel(
            deviceId=data.device_id,
            heartRate=data.heart_rate,
            oxygenLevel=data.oxygen_level,
            bodyTemperature=data.body_temperature,
            steps=data.steps,
            timestamp=data.timestamp
        )

        # Process via service
        result = await vital_service.ingest_vital_data(vital_input)

        # Broadcast for subscriptions
        await broadcast_vital(
            patient_id=data.device_id,
            heart_rate=data.heart_rate,
            oxygen_level=data.oxygen_level,
            body_temperature=data.body_temperature,
            steps=data.steps,
            timestamp=data.timestamp
        )

        return IngestResponse(
            status="ok",
            message="Vital data ingested",
            patient_id=result["patient_id"],
            patient_status=result["patient_status"]
        )

    @strawberry.mutation
    async def acknowledge_alert(self, alert_id: str) -> AckResponse:
        """
        Acknowledge an active alert
        Similar to POST /api/alerts/{id}/ack
        """
        try:
            result = await alert_service.acknowledge_alert(alert_id)
            return AckResponse(
                status="ok",
                message=f"Alert {alert_id} acknowledged",
                alert_id=result["alert_id"]
            )
        except AlertNotFoundError:
            return AckResponse(
                status="error",
                message=f"Alert {alert_id} not found",
                alert_id=alert_id
            )
        except AlertAlreadyAcknowledgedError:
            return AckResponse(
                status="error",
                message=f"Alert {alert_id} already acknowledged",
                alert_id=alert_id
            )

    @strawberry.mutation
    async def update_thresholds(self, thresholds: ThresholdInput) -> ThresholdType:
        """
        Update alert thresholds
        Similar to PUT /api/settings/thresholds
        """
        # Convert to domain model
        threshold_settings = ThresholdSettings(
            heart_rate_high=thresholds.heart_rate_high,
            heart_rate_low=thresholds.heart_rate_low,
            oxygen_level_low=thresholds.oxygen_level_low,
            body_temperature_high=thresholds.body_temperature_high,
            body_temperature_low=thresholds.body_temperature_low
        )

        await vital_service.update_thresholds(threshold_settings)

        return ThresholdType(
            heart_rate_high=thresholds.heart_rate_high,
            heart_rate_low=thresholds.heart_rate_low,
            oxygen_level_low=thresholds.oxygen_level_low,
            body_temperature_high=thresholds.body_temperature_high,
            body_temperature_low=thresholds.body_temperature_low
        )
