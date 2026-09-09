from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_officer
from app.models.user import User
from app.schemas.compliance_verification import (
    VerificationCreate,
    VerificationResponse,
)
from app.services.compliance_verification_service import (
    ComplianceVerificationService,
)
from app.services.inspection_service import InspectionService


router = APIRouter(
    prefix="/inspections",
    tags=["Verification"],
)


@router.post(
    "/{inspection_id}/verification",
    response_model=VerificationResponse,
)
def create_verification(
    inspection_id: int,
    data: VerificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_officer),
):
    InspectionService.get_owned_inspection(
        db=db,
        inspection_id=inspection_id,
        officer_id=current_user.id,
    )

    return ComplianceVerificationService.create_verification(
        db=db,
        inspection_id=inspection_id,
        officer_id=current_user.id,
        decision=data.decision,
        remarks=data.remarks,
    )
