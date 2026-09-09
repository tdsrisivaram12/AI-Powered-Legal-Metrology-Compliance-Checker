from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.evidence_service import EvidenceService
from app.services.inspection_service import InspectionService

router = APIRouter(
    prefix="/inspections",
    tags=["Evidence"],
)


@router.get("/{inspection_id}/evidence")
def get_evidence(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    InspectionService.get_owned_inspection(
        db=db,
        inspection_id=inspection_id,
        officer_id=current_user.id,
    )

    try:
        return EvidenceService.get_inspection_evidence(
            db,
            inspection_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
