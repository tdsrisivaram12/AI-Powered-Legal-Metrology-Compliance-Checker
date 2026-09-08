"""
Push notifications to the mobile/field app (e.g. FCM/APNs in production).
The provider call is abstracted behind PushProvider so swapping in a real
FCM client later doesn't change callers in services/api.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Protocol


@dataclass
class PushMessage:
    device_token: str
    title: str
    body: str
    data: Dict[str, str] = field(default_factory=dict)


class PushProvider(Protocol):
    def send(self, message: PushMessage) -> bool: ...


class MockPushProvider:
    """Default provider: records messages instead of calling a real push service."""

    def __init__(self):
        self.sent: List[PushMessage] = []

    def send(self, message: PushMessage) -> bool:
        self.sent.append(message)
        return True


class PushSender:
    def __init__(self, provider: Optional[PushProvider] = None):
        self.provider = provider or MockPushProvider()

    def notify_officer(self, device_token: str, inspection_id: str, decision: str) -> bool:
        message = PushMessage(
            device_token=device_token,
            title="Inspection result ready",
            body=f"Inspection {inspection_id}: {decision}",
            data={"inspection_id": inspection_id, "decision": decision},
        )
        return self.provider.send(message)

    def notify_new_assignment(self, device_token: str, inspection_id: str) -> bool:
        message = PushMessage(
            device_token=device_token,
            title="New inspection assigned",
            body=f"You have been assigned inspection {inspection_id}.",
            data={"inspection_id": inspection_id},
        )
        return self.provider.send(message)
