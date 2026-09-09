from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.inspection import Inspection
from app.repositories.inspection_repository import InspectionRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.inspection import InspectionCreate, InspectionUpdate


ALLOWED_INSPECTION_STATUSES = {
    "draft",
    "in_progress",
    "review",
    "completed",
    "closed",
}

ALLOWED_STATUS_TRANSITIONS = {
    "draft": {"draft", "in_progress"},
    "in_progress": {"in_progress", "review"},
    "review": {"review", "completed"},
    "completed": {"completed", "closed"},
    "closed": {"closed"},
}


class InspectionService:

    @staticmethod
    def create_inspection(
        db: Session,
        data: InspectionCreate,
        officer_id: int,
    ) -> Inspection:

        if data.status not in ALLOWED_INSPECTION_STATUSES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid inspection status: {data.status}",
            )

        existing = InspectionRepository.get_by_number(
            db,
            data.inspection_number,
        )

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Inspection number already exists",
            )

        if data.product_id is not None:
            product = ProductRepository.get_by_id(
                db,
                data.product_id,
            )

            if product is None:
                raise HTTPException(
                    status_code=404,
                    detail="Product not found",
                )

        return InspectionRepository.create(
            db,
            data,
            officer_id,
        )

    @staticmethod
    def get_inspection(
        db: Session,
        inspection_id: int,
    ) -> Inspection:

        inspection = InspectionRepository.get_by_id(
            db,
            inspection_id,
        )

        if inspection is None:
            raise HTTPException(
                status_code=404,
                detail="Inspection not found",
            )

        return inspection

    @staticmethod
    def get_owned_inspection(
        db: Session,
        inspection_id: int,
        officer_id: int,
    ) -> Inspection:

        inspection = InspectionService.get_inspection(
            db,
            inspection_id,
        )

        if inspection.officer_id != officer_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have access to this inspection",
            )

        return inspection

    @staticmethod
    def list_inspections(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Inspection]:

        if skip < 0:
            raise HTTPException(
                status_code=400,
                detail="skip cannot be negative",
            )

        if limit < 1 or limit > 100:
            raise HTTPException(
                status_code=400,
                detail="limit must be between 1 and 100",
            )

        return InspectionRepository.list(
            db,
            skip=skip,
            limit=limit,
        )

    @staticmethod
    def update_inspection(
        db: Session,
        inspection_id: int,
        data: InspectionUpdate,
        officer_id: int,
    ) -> Inspection:

        inspection = InspectionService.get_owned_inspection(
            db,
            inspection_id,
            officer_id,
        )

        if data.product_id is not None:
            product = ProductRepository.get_by_id(
                db,
                data.product_id,
            )

            if product is None:
                raise HTTPException(
                    status_code=404,
                    detail="Product not found",
                )

        updates = data.model_dump(exclude_unset=True)

        if "status" in updates:
            new_status = updates["status"]

            if new_status not in ALLOWED_INSPECTION_STATUSES:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid inspection status: {new_status}",
                )

            allowed_next = ALLOWED_STATUS_TRANSITIONS[
                inspection.status
            ]

            if new_status not in allowed_next:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Invalid status transition: "
                        f"{inspection.status} -> {new_status}"
                    ),
                )

            if new_status == "completed":
                updates["completed_at"] = datetime.now(timezone.utc)

            elif inspection.status == "completed" and new_status != "completed":
                updates["completed_at"] = None

        for field, value in updates.items():
            setattr(inspection, field, value)

        db.commit()
        db.refresh(inspection)

        return inspection
