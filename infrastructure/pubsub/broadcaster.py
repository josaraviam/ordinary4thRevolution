# infrastructure/pubsub/broadcaster.py
# In-memory pub/sub for GraphQL subscriptions

import asyncio
from typing import AsyncGenerator, Dict, Set, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class VitalUpdate:
    """Vital update message for subscriptions"""
    patient_id: str
    heart_rate: int
    oxygen_level: int
    body_temperature: float
    steps: int
    timestamp: datetime


class Broadcaster:
    """
    Simple in-memory broadcaster for real-time updates
    Used by GraphQL subscriptions to stream live data
    """

    def __init__(self):
        # Subscribers: channel -> set of queues
        self._subscribers: Dict[str, Set[asyncio.Queue]] = {}
        self._lock = asyncio.Lock()

    async def subscribe(self, channel: str) -> AsyncGenerator[Any, None]:
        """
        Subscribe to a channel and yield messages
        Usage: async for msg in broadcaster.subscribe("vitals"): ...
        """
        queue: asyncio.Queue = asyncio.Queue()

        async with self._lock:
            if channel not in self._subscribers:
                self._subscribers[channel] = set()
            self._subscribers[channel].add(queue)

        try:
            while True:
                message = await queue.get()
                yield message
        finally:
            # Cleanup on disconnect
            async with self._lock:
                self._subscribers[channel].discard(queue)
                if not self._subscribers[channel]:
                    del self._subscribers[channel]

    async def publish(self, channel: str, message: Any):
        """
        Publish message to all subscribers on a channel
        """
        async with self._lock:
            if channel in self._subscribers:
                for queue in self._subscribers[channel]:
                    try:
                        queue.put_nowait(message)
                    except asyncio.QueueFull:
                        # Skip if queue is full (slow consumer)
                        pass

    async def publish_vital_update(self, update: VitalUpdate):
        """
        Publish vital update to the vitals channel
        Called after ingesting new vital data
        """
        await self.publish("vitals", update)

    def get_subscriber_count(self, channel: str) -> int:
        """Get number of active subscribers on a channel"""
        return len(self._subscribers.get(channel, set()))


# Singleton broadcaster instance
broadcaster = Broadcaster()


# Helper function to publish vitals (used by vital_service)
async def broadcast_vital(
    patient_id: str,
    heart_rate: int,
    oxygen_level: int,
    body_temperature: float,
    steps: int,
    timestamp: datetime
):
    """Convenience function to broadcast vital update"""
    update = VitalUpdate(
        patient_id=patient_id,
        heart_rate=heart_rate,
        oxygen_level=oxygen_level,
        body_temperature=body_temperature,
        steps=steps,
        timestamp=timestamp
    )
    await broadcaster.publish_vital_update(update)
