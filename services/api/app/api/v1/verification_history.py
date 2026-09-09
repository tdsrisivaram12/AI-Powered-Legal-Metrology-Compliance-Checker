from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.compliance_verification_service import (
    ComplianceVerificationService,
)
from app.services.inspection_service import InspectionService


router = APIRouter(
    prefix="/inspections",
    tags=["Verification History"],
)


@router.get("/{inspection_id}/verifications")
def list_verifications(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    InspectionService.get_owned_inspection(
        db=db,
        inspection_id=inspection_id,
        officer_id=current_user.id,
    )

    return ComplianceVerificationService.list_verifications(
        db,
        inspection_id,
    )
