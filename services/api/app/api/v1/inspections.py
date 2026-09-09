from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, require_officer
from app.models.user import User
from app.schemas.inspection import (
    InspectionCreate,
    InspectionResponse,
    InspectionUpdate,
)
from app.services.inspection_service import InspectionService


router = APIRouter(
    prefix="/inspections",
    tags=["Inspections"],
)


@router.post(
    "",
    response_model=InspectionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_inspection(
    data: InspectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_officer),
) -> InspectionResponse:
    return InspectionService.create_inspection(
        db=db,
        data=data,
        officer_id=current_user.id,
    )


@router.get(
    "",
    response_model=list[InspectionResponse],
)
def list_inspections(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[InspectionResponse]:
    return InspectionService.list_inspections(
        db=db,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{inspection_id}",
    response_model=InspectionResponse,
)
def get_inspection(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> InspectionResponse:
    return InspectionService.get_inspection(
        db=db,
        inspection_id=inspection_id,
    )


@router.patch(
    "/{inspection_id}",
    response_model=InspectionResponse,
)
def update_inspection(
    inspection_id: int,
    data: InspectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_officer),
) -> InspectionResponse:
    return InspectionService.update_inspection(
        db=db,
        inspection_id=inspection_id,
        data=data,
        officer_id=current_user.id,
    )
