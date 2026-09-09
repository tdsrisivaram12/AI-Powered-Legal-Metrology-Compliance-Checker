from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inspection import Inspection
from app.schemas.inspection import InspectionCreate, InspectionUpdate


class InspectionRepository:

    @staticmethod
    def get_by_id(
        db: Session,
        inspection_id: int,
    ) -> Inspection | None:
        return db.get(Inspection, inspection_id)

    @staticmethod
    def get_by_number(
        db: Session,
        inspection_number: str,
    ) -> Inspection | None:
        return db.scalar(
            select(Inspection).where(
                Inspection.inspection_number == inspection_number
            )
        )

    @staticmethod
    def list(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Inspection]:
        return list(
            db.scalars(
                select(Inspection)
                .order_by(Inspection.created_at.desc())
                .offset(skip)
                .limit(limit)
            ).all()
        )

    @staticmethod
    def create(
        db: Session,
        data: InspectionCreate,
        officer_id: int,
    ) -> Inspection:

        inspection = Inspection(
            inspection_number=data.inspection_number,
            officer_id=officer_id,
            product_id=data.product_id,
            status=data.status,
            notes=data.notes,
        )

        db.add(inspection)
        db.commit()
        db.refresh(inspection)

        return inspection

    @staticmethod
    def update(
        db: Session,
        inspection: Inspection,
        data: InspectionUpdate,
    ) -> Inspection:

        for field, value in data.model_dump(
            exclude_unset=True
        ).items():
            setattr(inspection, field, value)

        db.commit()
        db.refresh(inspection)

        return inspection
