from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.compliance_verification import ComplianceVerification
from app.models.inspection import Inspection
from app.models.user import User


class ComplianceVerificationService:

    @staticmethod
    def create_verification(
        db: Session,
        inspection_id: int,
        officer_id: int,
        decision: str,
        remarks: str | None = None,
    ) -> ComplianceVerification:

        inspection = db.get(Inspection, inspection_id)

        if inspection is None:
            raise HTTPException(
                status_code=404,
                detail="Inspection not found",
            )

        officer = db.get(User, officer_id)

        if officer is None or not officer.is_active:
            raise HTTPException(
                status_code=404,
                detail="Officer not found",
            )

        verification = ComplianceVerification(
            inspection_id=inspection_id,
            officer_id=officer_id,
            decision=decision,
            remarks=remarks,
        )

        db.add(verification)
        db.commit()
        db.refresh(verification)

        return verification

    @staticmethod
    def list_verifications(
        db: Session,
        inspection_id: int,
    ):
        inspection = db.get(Inspection, inspection_id)

        if inspection is None:
            raise HTTPException(
                status_code=404,
                detail="Inspection not found",
            )

        return (
            db.query(ComplianceVerification)
            .filter(
                ComplianceVerification.inspection_id == inspection_id
            )
            .order_by(ComplianceVerification.verified_at.desc())
            .all()
        )
