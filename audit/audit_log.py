"""
Append-only audit trail for evidence chain-of-custody: who captured it, who
viewed it, who annotated it, when the officer verified a finding, etc.
Each entry is hash-chained to the previous entry so the log itself is
tamper-evident (classic blockchain-style linking, no external ledger needed).
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import List, Optional

from services.evidence.hashing.hashing import hash_bytes

GENESIS_HASH = "0" * 64


@dataclass
class AuditEntry:
    inspection_id: str
    evidence_id: str
    action: str          # e.g. "CAPTURED", "VIEWED", "ANNOTATED", "OFFICER_VERIFIED"
    actor: str            # user id / role
    timestamp: str
    prev_hash: str
    entry_hash: str = field(default="")
    details: Optional[str] = None


class AuditLog:
    def __init__(self):
        self._entries: List[AuditEntry] = []

    def record(self, inspection_id: str, evidence_id: str, action: str, actor: str, details: str = "") -> AuditEntry:
        prev_hash = self._entries[-1].entry_hash if self._entries else GENESIS_HASH
        timestamp = datetime.now(timezone.utc).isoformat()

        payload = f"{inspection_id}|{evidence_id}|{action}|{actor}|{timestamp}|{prev_hash}|{details}"
        entry_hash = hash_bytes(payload.encode("utf-8"))

        entry = AuditEntry(
            inspection_id=inspection_id,
            evidence_id=evidence_id,
            action=action,
            actor=actor,
            timestamp=timestamp,
            prev_hash=prev_hash,
            entry_hash=entry_hash,
            details=details,
        )
        self._entries.append(entry)
        return entry

    def verify_chain(self) -> bool:
        prev = GENESIS_HASH
        for e in self._entries:
            if e.prev_hash != prev:
                return False
            payload = f"{e.inspection_id}|{e.evidence_id}|{e.action}|{e.actor}|{e.timestamp}|{e.prev_hash}|{e.details}"
            if hash_bytes(payload.encode("utf-8")) != e.entry_hash:
                return False
            prev = e.entry_hash
        return True

    def history_for(self, evidence_id: str) -> List[AuditEntry]:
        return [e for e in self._entries if e.evidence_id == evidence_id]

    def to_json(self) -> str:
        return json.dumps([asdict(e) for e in self._entries], indent=2)
