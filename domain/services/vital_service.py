from datetime import datetime
from typing import List, Optional

from domain.models.vital import (
    VitalDataInput, VitalResponse, VitalListResponse,
    AlertResponse, AlertListResponse, ThresholdSettings
)
from domain.exceptions.custom_exceptions import (
    AlertNotFoundError,
    AlertAlreadyAcknowledgedError,
    PatientNotFoundError,
)
from infrastructure.database.repositories.vital_repository import (
    vital_repo, alert_repo, settings_repo
)
from infrastructure.database.repositories.patient_repository import patient_repo
from config.constants import PatientStatus, AlertType, AlertStatus, DEFAULT_THRESHOLDS


class VitalService:
    """
    Vital service layer
    Handles vital data ingestion, alerts, and thresholds
    """

    async def get_thresholds(self) -> ThresholdSettings:
        """Get current alert thresholds"""
        thresholds = await settings_repo.get_thresholds()

        if thresholds:
            return ThresholdSettings(
                heart_rate_high=thresholds.get("heart_rate_high", DEFAULT_THRESHOLDS["heart_rate_high"]),
                heart_rate_low=thresholds.get("heart_rate_low", DEFAULT_THRESHOLDS["heart_rate_low"]),
                oxygen_level_low=thresholds.get("oxygen_level_low", DEFAULT_THRESHOLDS["oxygen_level_low"]),
                body_temperature_high=thresholds.get("body_temperature_high", DEFAULT_THRESHOLDS["body_temperature_high"]),
                body_temperature_low=thresholds.get("body_temperature_low", DEFAULT_THRESHOLDS["body_temperature_low"]),
            )

        return ThresholdSettings(**DEFAULT_THRESHOLDS)

    async def check_and_create_alerts(
        self,
        patient_id: str,
        heart_rate: int,
        oxygen_level: int,
        body_temp: float
    ) -> str:
        """
        Check vitals against thresholds and create alerts
        Returns patient status: OK or ALERT
        """
        thresholds = await self.get_thresholds()
        alerts_created = []

        # Heart rate HIGH
        if heart_rate > thresholds.heart_rate_high:
            await alert_repo.create({
                "patient_id": patient_id,
                "metric": "heart_rate",
                "type": AlertType.HIGH,
                "value": heart_rate,
                "threshold": thresholds.heart_rate_high
            })
            alerts_created.append("HR_HIGH")

        # Heart rate LOW
        if heart_rate < thresholds.heart_rate_low:
            await alert_repo.create({
                "patient_id": patient_id,
                "metric": "heart_rate",
                "type": AlertType.LOW,
                "value": heart_rate,
                "threshold": thresholds.heart_rate_low
            })
            alerts_created.append("HR_LOW")

        # Oxygen LOW
        if oxygen_level < thresholds.oxygen_level_low:
            await alert_repo.create({
                "patient_id": patient_id,
                "metric": "oxygen_level",
                "type": AlertType.LOW,
                "value": oxygen_level,
                "threshold": thresholds.oxygen_level_low
            })
            alerts_created.append("O2_LOW")

        # Temperature HIGH
        if body_temp > thresholds.body_temperature_high:
            await alert_repo.create({
                "patient_id": patient_id,
                "metric": "body_temperature",
                "type": AlertType.HIGH,
                "value": body_temp,
                "threshold": thresholds.body_temperature_high
            })
            alerts_created.append("TEMP_HIGH")

        # Temperature LOW
        if body_temp < thresholds.body_temperature_low:
            await alert_repo.create({
                "patient_id": patient_id,
                "metric": "body_temperature",
                "type": AlertType.LOW,
                "value": body_temp,
                "threshold": thresholds.body_temperature_low
            })
            alerts_created.append("TEMP_LOW")

        return PatientStatus.ALERT if alerts_created else PatientStatus.OK

    async def ingest_vital_data(self, data: VitalDataInput) -> dict:
        """
        Process incoming vital data from Node-RED
        Creates/updates patient, checks thresholds, stores reading
        """
        patient_id = data.deviceId

        # Ensure patient exists
        await patient_repo.upsert_by_patient_id(
            patient_id=patient_id,
            data={"patient_name": f"Patient {patient_id}"}
        )

        # Check thresholds and create alerts
        patient_status = await self.check_and_create_alerts(
            patient_id=patient_id,
            heart_rate=data.heartRate,
            oxygen_level=data.oxygenLevel,
            body_temp=data.bodyTemperature
        )

        # Update patient's latest vitals
        await patient_repo.update_latest_vitals(
            patient_id=patient_id,
            heart_rate=data.heartRate,
            oxygen_level=data.oxygenLevel,
            body_temp=data.bodyTemperature,
            steps=data.steps,
            status=patient_status
        )

        # Store vital reading
        vital_doc = {
            "patient_id": patient_id,
            "heart_rate": data.heartRate,
            "oxygen_level": data.oxygenLevel,
            "body_temperature": data.bodyTemperature,
            "steps": data.steps,
            "timestamp": data.timestamp,
            "created_at": datetime.utcnow()
        }
        await vital_repo.create(vital_doc)

        return {
            "patient_id": patient_id,
            "patient_status": patient_status
        }

    async def get_patient_readings(
        self,
        patient_id: str,
        limit: int = 10
    ) -> VitalListResponse:
        """Get recent readings for a patient"""
        readings = await vital_repo.find_by_patient(patient_id, limit=limit)
        total = await vital_repo.count_by_patient(patient_id)

        items = []
        for r in readings:
            items.append(VitalResponse(
                id=str(r["_id"]),
                patient_id=r["patient_id"],
                heart_rate=r["heart_rate"],
                oxygen_level=r["oxygen_level"],
                body_temperature=r["body_temperature"],
                steps=r["steps"],
                timestamp=r["timestamp"]
            ))

        return VitalListResponse(items=items, total=total)

    async def update_thresholds(self, thresholds: ThresholdSettings) -> bool:
        """Update alert thresholds"""
        return await settings_repo.upsert_thresholds(thresholds.model_dump())


class AlertService:
    """
    Alert service layer
    Handles alert retrieval and acknowledgement
    """

    async def get_alerts(
        self,
        status_filter: Optional[str] = None,
        skip: int = 0,
        limit: int = 50
    ) -> AlertListResponse:
        """Get alerts, optionally filtered by status"""
        if status_filter:
            alerts = await alert_repo.find_by_status(status_filter, skip=skip, limit=limit)
        else:
            alerts = await alert_repo.find_active(skip=skip, limit=limit)

        total = await alert_repo.count_active()

        items = []
        for a in alerts:
            items.append(AlertResponse(
                id=str(a["_id"]),
                alert_id=a["alert_id"],
                patient_id=a["patient_id"],
                metric=a["metric"],
                type=a["type"],
                value=a["value"],
                threshold=a["threshold"],
                status=a["status"],
                created_at=a["created_at"],
                acknowledged_at=a.get("acknowledged_at")
            ))

        return AlertListResponse(items=items, total=total)

    async def acknowledge_alert(self, alert_id: str) -> dict:
        """
        Acknowledge an active alert
        Raises: AlertNotFoundError, AlertAlreadyAcknowledgedError
        """
        # Check alert exists
        alert = await alert_repo.find_by_alert_id(alert_id)
        if not alert:
            raise AlertNotFoundError(alert_id)

        # Check if already ack'd
        if alert["status"] != AlertStatus.ACTIVE:
            raise AlertAlreadyAcknowledgedError(alert_id)

        # Acknowledge
        success = await alert_repo.acknowledge(alert_id)
        if not success:
            raise AlertNotFoundError(alert_id)

        return {"alert_id": alert_id, "status": "acknowledged"}

    async def get_active_count(self) -> int:
        """Get count of active alerts"""
        return await alert_repo.count_active()

    async def get_alert_count_in_window(self, minutes: int = 5) -> int:
        """Get alert count in time window"""
        return await alert_repo.count_in_window(minutes=minutes)


class ReportService:
    """
    Report service layer
    Handles KPIs and data exports
    """

    async def get_kpis(self, window_minutes: int = 5) -> dict:
        """Get dashboard KPIs"""
        patients_monitored = await patient_repo.count_active()
        active_alerts = await alert_repo.count_active()
        avg_hr = await vital_repo.get_avg_heart_rate(minutes=window_minutes)

        return {
            "patients_monitored": patients_monitored,
            "active_alerts": active_alerts,
            "average_heart_rate": avg_hr or 0,
            "window_minutes": window_minutes
        }

    async def get_summary(
        self,
        window_minutes: int = 5,
        patient_id: Optional[str] = None
    ) -> dict:
        """Get aggregated stats for time window"""
        avg_hr = await vital_repo.get_avg_heart_rate(minutes=window_minutes)
        min_o2 = await vital_repo.get_min_oxygen(minutes=window_minutes)
        alert_count = await alert_repo.count_in_window(minutes=window_minutes)

        return {
            "average_heart_rate": avg_hr or 0,
            "minimum_oxygen_level": min_o2 or 0,
            "alert_count": alert_count,
            "window_minutes": window_minutes
        }

    async def get_readings_for_export(
        self,
        window_minutes: int = 5,
        patient_id: Optional[str] = None
    ) -> List[dict]:
        """Get readings for CSV export"""
        return await vital_repo.get_readings_in_window(
            minutes=window_minutes,
            patient_id=patient_id
        )


# Singleton instances
vital_service = VitalService()
alert_service = AlertService()
report_service = ReportService()
