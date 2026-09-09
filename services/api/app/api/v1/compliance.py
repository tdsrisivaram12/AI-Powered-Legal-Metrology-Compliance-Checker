from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.compliance_evaluator import ComplianceEvaluator

router = APIRouter(
    prefix="/inspections",
    tags=["Compliance"],
)


@router.get("/{inspection_id}/compliance")
def evaluate_compliance(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return ComplianceEvaluator.evaluate_inspection(
            db,
            inspection_id,
        )
    except ValueError as exc:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
