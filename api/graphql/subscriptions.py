# api/graphql/subscriptions.py
# GraphQL subscriptions for real-time data

import strawberry
from typing import AsyncGenerator

from api.graphql.types import LiveVitalsType
from infrastructure.pubsub.broadcaster import broadcaster, VitalUpdate


@strawberry.type
class Subscription:
    """Root GraphQL subscriptions"""

    @strawberry.subscription
    async def live_vitals(self) -> AsyncGenerator[LiveVitalsType, None]:
        """
        Subscribe to live vital updates
        subscription { liveVitals { id heartRate oxygenLevel bodyTemperature steps } }

        Streams real-time data whenever new vitals are ingested
        """
        async for update in broadcaster.subscribe("vitals"):
            if isinstance(update, VitalUpdate):
                yield LiveVitalsType(
                    id=update.patient_id,
                    heart_rate=update.heart_rate,
                    oxygen_level=update.oxygen_level,
                    body_temperature=update.body_temperature,
                    steps=update.steps,
                    timestamp=update.timestamp
                )

    @strawberry.subscription
    async def patient_vitals(
        self,
        patient_id: str
    ) -> AsyncGenerator[LiveVitalsType, None]:
        """
        Subscribe to live vitals for a specific patient
        subscription { patientVitals(patientId: "P-101") { heartRate oxygenLevel } }
        """
        async for update in broadcaster.subscribe("vitals"):
            if isinstance(update, VitalUpdate):
                # Filter by patient_id
                if update.patient_id == patient_id:
                    yield LiveVitalsType(
                        id=update.patient_id,
                        heart_rate=update.heart_rate,
                        oxygen_level=update.oxygen_level,
                        body_temperature=update.body_temperature,
                        steps=update.steps,
                        timestamp=update.timestamp
                    )
