from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_officer
from app.models.user import User
from app.schemas.inspection_image import InspectionImageResponse
from app.services.inspection_image_service import InspectionImageService
from app.services.inspection_service import InspectionService


router = APIRouter(
    prefix="/inspections",
    tags=["Inspection Images"],
)


@router.post(
    "/{inspection_id}/images",
    response_model=InspectionImageResponse,
)
async def upload_inspection_image(
    inspection_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_officer),
):
    InspectionService.get_owned_inspection(
        db=db,
        inspection_id=inspection_id,
        officer_id=current_user.id,
    )

    return await InspectionImageService.upload_image(
        db=db,
        inspection_id=inspection_id,
        file=file,
    )
