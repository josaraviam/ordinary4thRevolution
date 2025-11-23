# domain/services/patient_service.py
# Patient business logic - this is where the magic happens
# Sits between the API routes and the database (clean architecture style)

from typing import List, Optional

from domain.models.patient import PatientResponse, PatientListResponse
from domain.exceptions.custom_exceptions import PatientNotFoundError
from infrastructure.database.repositories.patient_repository import patient_repo


class PatientService:
    """
    Patient service layer - handles all patient-related business logic
    the "brain" between the API and the database.
    """

    async def get_all_patients(
        self,
        page: int = 1,        # Which page (starts at 1, not 0 - user friendly)
        page_size: int = 20   # How many per page (20 seems reasonable)
    ) -> PatientListResponse:
        """ 
        Returns a paginated response so the frontend doesn't crash
        when we have thousands of patients ( we won't get there with this demo but still useful)
        """
        skip = (page - 1) * page_size  # Convert page number to skip count
        patients = await patient_repo.find_all(skip=skip, limit=page_size)
        total = await patient_repo.count_all()  # For pagination info

        items = []  # Build our response list
        for p in patients:
            # Convert MongoDB doc to our nice response model
            items.append(PatientResponse(
                id=str(p["_id"]),  # MongoDB ObjectId to string
                patient_id=p["patient_id"],
                patient_name=p.get("patient_name", "Unknown"),  # Fallback if missing
                status=p.get("status", "OK"),                   # Default to OK
                last_heart_rate=p.get("last_heart_rate"),
                last_oxygen_level=p.get("last_oxygen_level"),
                last_body_temperature=p.get("last_body_temperature"),
                last_steps=p.get("last_steps"),
                last_update=p.get("last_update")
            ))

        return PatientListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size
        )

    async def get_patient_by_id(self, patient_id: str) -> PatientResponse:
        """
        Get single patient by patient_id
        Raises: PatientNotFoundError if not found
        """
        patient = await patient_repo.find_by_patient_id(patient_id)
        if patient is None:
            raise PatientNotFoundError(patient_id)

        return PatientResponse(
            id=str(patient["_id"]),
            patient_id=patient["patient_id"],
            patient_name=patient.get("patient_name", "Unknown"),
            status=patient.get("status", "OK"),
            last_heart_rate=patient.get("last_heart_rate"),
            last_oxygen_level=patient.get("last_oxygen_level"),
            last_body_temperature=patient.get("last_body_temperature"),
            last_steps=patient.get("last_steps"),
            last_update=patient.get("last_update")
        )

    async def ensure_patient_exists(self, patient_id: str, name: str = None) -> str:
        """
        Ensure patient exists, create if not
        Returns patient document id
        """
        default_name = name or f"Patient {patient_id}"
        return await patient_repo.upsert_by_patient_id(
            patient_id=patient_id,
            data={"patient_name": default_name}
        )

    async def update_patient_vitals(
        self,
        patient_id: str,
        heart_rate: int,
        oxygen_level: int,
        body_temp: float,
        steps: int,
        status: str
    ):
        """Update patient's latest vital readings and status"""
        await patient_repo.update_latest_vitals(
            patient_id=patient_id,
            heart_rate=heart_rate,
            oxygen_level=oxygen_level,
            body_temp=body_temp,
            steps=steps,
            status=status
        )

    async def get_monitored_count(self) -> int:
        """Get count of patients with recent updates"""
        return await patient_repo.count_active()


# Singleton instance
patient_service = PatientService()
