from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.inspection_pdf_service import InspectionPDFService
from app.services.inspection_service import InspectionService

router = APIRouter(
    prefix="/inspections",
    tags=["Reports"],
)


@router.get("/{inspection_id}/report/pdf")
def download_inspection_report(
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
        pdf_path = InspectionPDFService.generate_pdf(
            db,
            inspection_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    if not pdf_path.exists():
        raise HTTPException(
            status_code=500,
            detail="Generated PDF was not found",
        )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=pdf_path.name,
    )
