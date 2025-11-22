# api/graphql/queries.py
# GraphQL queries

import strawberry
from typing import List, Optional

from api.graphql.types import (
    PatientType, VitalType, AlertType,
    ThresholdType, KPIType, SummaryType
)
from domain.services.patient_service import patient_service
from domain.services.vital_service import vital_service, alert_service, report_service


@strawberry.type
class Query:
    """Root GraphQL queries"""

    @strawberry.field
    async def patients(
        self,
        page: int = 1,
        page_size: int = 20
    ) -> List[PatientType]:
        """
        Get all patients with latest metrics
        query { patients { id name heartRate oxygenLevel bodyTemperature } }
        """
        result = await patient_service.get_all_patients(page=page, page_size=page_size)

        return [
            PatientType(
                id=p.id or "",
                name=p.patient_name,
                patient_id=p.patient_id,
                status=p.status,
                heart_rate=p.last_heart_rate,
                oxygen_level=p.last_oxygen_level,
                body_temperature=p.last_body_temperature,
                steps=p.last_steps,
                last_update=p.last_update
            )
            for p in result.items
        ]

    @strawberry.field
    async def patient(self, patient_id: str) -> Optional[PatientType]:
        """Get single patient by ID"""
        try:
            p = await patient_service.get_patient_by_id(patient_id)
            return PatientType(
                id=p.id or "",
                name=p.patient_name,
                patient_id=p.patient_id,
                status=p.status,
                heart_rate=p.last_heart_rate,
                oxygen_level=p.last_oxygen_level,
                body_temperature=p.last_body_temperature,
                steps=p.last_steps,
                last_update=p.last_update
            )
        except Exception:
            return None

    @strawberry.field
    async def patient_readings(
        self,
        patient_id: str,
        limit: int = 10
    ) -> List[VitalType]:
        """Get recent readings for a patient"""
        result = await vital_service.get_patient_readings(patient_id, limit=limit)

        return [
            VitalType(
                id=v.id or "",
                patient_id=v.patient_id,
                heart_rate=v.heart_rate,
                oxygen_level=v.oxygen_level,
                body_temperature=v.body_temperature,
                steps=v.steps,
                timestamp=v.timestamp
            )
            for v in result.items
        ]

    @strawberry.field
    async def alerts(
        self,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[AlertType]:
        """Get alerts, optionally filtered by status"""
        result = await alert_service.get_alerts(
            status_filter=status,
            skip=0,
            limit=limit
        )

        return [
            AlertType(
                id=a.id or "",
                alert_id=a.alert_id,
                patient_id=a.patient_id,
                metric=a.metric,
                type=a.type,
                value=a.value,
                threshold=a.threshold,
                status=a.status,
                created_at=a.created_at,
                acknowledged_at=a.acknowledged_at
            )
            for a in result.items
        ]

    @strawberry.field
    async def thresholds(self) -> ThresholdType:
        """Get current alert thresholds"""
        t = await vital_service.get_thresholds()
        return ThresholdType(
            heart_rate_high=t.heart_rate_high,
            heart_rate_low=t.heart_rate_low,
            oxygen_level_low=t.oxygen_level_low,
            body_temperature_high=t.body_temperature_high,
            body_temperature_low=t.body_temperature_low
        )

    @strawberry.field
    async def kpis(self, window_minutes: int = 5) -> KPIType:
        """Get dashboard KPIs"""
        result = await report_service.get_kpis(window_minutes=window_minutes)
        return KPIType(
            patients_monitored=result["patients_monitored"],
            active_alerts=result["active_alerts"],
            average_heart_rate=result["average_heart_rate"],
            window_minutes=result["window_minutes"]
        )

    @strawberry.field
    async def summary(
        self,
        window_minutes: int = 5,
        patient_id: Optional[str] = None
    ) -> SummaryType:
        """Get report summary"""
        result = await report_service.get_summary(
            window_minutes=window_minutes,
            patient_id=patient_id
        )
        return SummaryType(
            average_heart_rate=result["average_heart_rate"],
            minimum_oxygen_level=result["minimum_oxygen_level"],
            alert_count=result["alert_count"],
            window_minutes=result["window_minutes"]
        )
