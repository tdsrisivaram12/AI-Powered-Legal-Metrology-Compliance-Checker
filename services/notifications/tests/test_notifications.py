import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from services.notifications.email.email_sender import EmailSender
from services.notifications.push.push_sender import MockPushProvider, PushSender


def test_email_dry_run_records_outbox_without_network():
    sender = EmailSender(dry_run=True)
    record = sender.send_violation_alert(
        to=["inspector@example.gov.in"], product_id="PROD-001",
        decision="SUSPECTED NON-COMPLIANCE", findings_count=2,
    )
    assert record.dry_run is True
    assert len(sender.outbox) == 1
    assert "PROD-001" in sender.outbox[0].subject


def test_push_notify_officer_uses_mock_provider():
    provider = MockPushProvider()
    sender = PushSender(provider=provider)
    ok = sender.notify_officer("device-token-123", "INSP-1", "REVIEW")
    assert ok is True
    assert len(provider.sent) == 1
    assert provider.sent[0].data["inspection_id"] == "INSP-1"


def test_push_notify_new_assignment():
    provider = MockPushProvider()
    sender = PushSender(provider=provider)
    sender.notify_new_assignment("device-token-456", "INSP-2")
    assert provider.sent[0].title == "New inspection assigned"


if __name__ == "__main__":
    test_email_dry_run_records_outbox_without_network()
    test_push_notify_officer_uses_mock_provider()
    test_push_notify_new_assignment()
    print("All notification tests passed.")
