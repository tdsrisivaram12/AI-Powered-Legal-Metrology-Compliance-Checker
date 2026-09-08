"""
Content-addressed evidence storage. Files are stored under
<base_dir>/<inspection_id>/<hash>.<ext> so the same image can never
silently overwrite another, and the returned EvidenceRecord always carries
the integrity hash computed at save time.

In production this would target S3/GCS instead of local disk; the interface
(save/get/exists) is kept small on purpose so swapping the backend later
doesn't require touching callers in services/api.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from services.evidence.hashing.hashing import hash_bytes

DEFAULT_BASE_DIR = Path("evidence_store")


@dataclass
class EvidenceRecord:
    evidence_id: str
    inspection_id: str
    file_path: str
    sha256: str
    content_type: str
    stored_at: str


class EvidenceStorage:
    def __init__(self, base_dir: str | Path = DEFAULT_BASE_DIR):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save(
        self,
        inspection_id: str,
        file_bytes: bytes,
        original_filename: str,
        content_type: str = "image/jpeg",
    ) -> EvidenceRecord:
        digest = hash_bytes(file_bytes)
        ext = Path(original_filename).suffix or ".bin"
        inspection_dir = self.base_dir / inspection_id
        inspection_dir.mkdir(parents=True, exist_ok=True)

        dest = inspection_dir / f"{digest}{ext}"
        if not dest.exists():
            dest.write_bytes(file_bytes)

        return EvidenceRecord(
            evidence_id=digest,
            inspection_id=inspection_id,
            file_path=str(dest),
            sha256=digest,
            content_type=content_type,
            stored_at=datetime.now(timezone.utc).isoformat(),
        )

    def get(self, inspection_id: str, evidence_id: str, ext: str) -> bytes:
        path = self.base_dir / inspection_id / f"{evidence_id}{ext}"
        return path.read_bytes()

    def exists(self, inspection_id: str, evidence_id: str, ext: str) -> bool:
        return (self.base_dir / inspection_id / f"{evidence_id}{ext}").exists()
