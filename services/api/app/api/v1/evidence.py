"""
POST /api/v1/evidence/upload -- stores an evidence file (e.g. a package
photo captured during inspection) and records the CAPTURED audit event.
GET  /api/v1/evidence/{inspection_id}/{evidence_id}/audit -- chain-of-custody.
"""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from services.api.app.core.dependencies import audit_log, evidence_storage

router = APIRouter(prefix="/api/v1/evidence", tags=["evidence"])


class EvidenceUploadOut(BaseModel):
    evidence_id: str
    inspection_id: str
    sha256: str
    content_type: str
    stored_at: str


class AuditEntryOut(BaseModel):
    action: str
    actor: str
    timestamp: str
    entry_hash: str
    details: str | None = None


@router.post("/upload", response_model=EvidenceUploadOut)
async def upload_evidence(
    inspection_id: str = Form(...),
    actor: str = Form(...),
    file: UploadFile = File(...),
):
    file_bytes = await file.read()
    record = evidence_storage.save(
        inspection_id=inspection_id,
        file_bytes=file_bytes,
        original_filename=file.filename or "upload.jpg",
        content_type=file.content_type or "image/jpeg",
    )
    audit_log.record(
        inspection_id=inspection_id,
        evidence_id=record.evidence_id,
        action="CAPTURED",
        actor=actor,
        details=f"Uploaded {file.filename}",
    )
    return EvidenceUploadOut(
        evidence_id=record.evidence_id,
        inspection_id=record.inspection_id,
        sha256=record.sha256,
        content_type=record.content_type,
        stored_at=record.stored_at,
    )


@router.get("/{inspection_id}/{evidence_id}/audit", response_model=List[AuditEntryOut])
def get_audit_trail(inspection_id: str, evidence_id: str):
    entries = audit_log.history_for(evidence_id)
    if not entries:
        raise HTTPException(status_code=404, detail="No audit history found for this evidence_id")
    return [
        AuditEntryOut(action=e.action, actor=e.actor, timestamp=e.timestamp, entry_hash=e.entry_hash, details=e.details)
        for e in entries
    ]


@router.get("/verify-chain")
def verify_chain():
    return {"valid": audit_log.verify_chain()}
