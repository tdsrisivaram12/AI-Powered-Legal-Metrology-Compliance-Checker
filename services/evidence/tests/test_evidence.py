import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from services.evidence.annotation.annotation import Annotation, AnnotatedEvidence, BoundingBox
from services.evidence.audit.audit_log import AuditLog
from services.evidence.hashing.hashing import hash_bytes, hash_file, verify_file
from services.evidence.storage.storage import EvidenceStorage


def test_storage_is_content_addressed():
    with tempfile.TemporaryDirectory() as tmp:
        storage = EvidenceStorage(base_dir=tmp)
        record = storage.save("INSP-1", b"fake image bytes", "front.jpg", "image/jpeg")
        assert record.sha256 == hash_bytes(b"fake image bytes")
        assert storage.exists("INSP-1", record.evidence_id, ".jpg")
        # saving identical bytes again should not create a duplicate error and hash matches
        record2 = storage.save("INSP-1", b"fake image bytes", "front2.jpg", "image/jpeg")
        assert record.sha256 == record2.sha256


def test_hash_file_roundtrip():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"legal metrology evidence")
        tmp_path = tmp.name
    digest = hash_file(tmp_path)
    assert verify_file(tmp_path, digest)
    assert not verify_file(tmp_path, "0" * 64)


def test_annotation_links_to_rule():
    evidence = AnnotatedEvidence(evidence_id="abc123")
    evidence.add(Annotation(
        evidence_id="abc123",
        label="Missing MRP",
        rule_id="LM-MRP-001",
        box=BoundingBox(x=0.1, y=0.1, width=0.3, height=0.1),
        note="No MRP text detected in this region.",
    ))
    assert len(evidence.for_rule("LM-MRP-001")) == 1
    assert evidence.for_rule("LM-NETQTY-001") == []


def test_audit_chain_is_verifiable_and_detects_tampering():
    log = AuditLog()
    log.record("INSP-1", "abc123", "CAPTURED", actor="officer_1")
    log.record("INSP-1", "abc123", "ANNOTATED", actor="ai_pipeline", details="LM-MRP-001 violation")
    log.record("INSP-1", "abc123", "OFFICER_VERIFIED", actor="officer_1")
    assert log.verify_chain() is True

    # tamper with an entry directly and confirm detection
    log._entries[1].details = "tampered"
    assert log.verify_chain() is False


if __name__ == "__main__":
    test_storage_is_content_addressed()
    test_hash_file_roundtrip()
    test_annotation_links_to_rule()
    test_audit_chain_is_verifiable_and_detects_tampering()
    print("All evidence tests passed.")
