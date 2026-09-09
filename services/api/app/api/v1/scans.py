from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_officer
from app.models.user import User
from app.models.ocr_result import OCRResult
from app.models.declaration import Declaration
from app.schemas.scan import ScanCreate, ScanResponse
from app.services.scan_service import ScanService
from app.services.ocr_service import OCRService
from app.services.declaration_extraction_service import DeclarationExtractionService
from app.services.compliance_evaluator import ComplianceEvaluator
from app.services.inspection_service import InspectionService


router = APIRouter(
    prefix="/inspections",
    tags=["Scans"],
)


@router.post(
    "/{inspection_id}/scans",
    response_model=ScanResponse,
)
def create_scan(
    inspection_id: int,
    data: ScanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_officer),
):
    InspectionService.get_owned_inspection(
        db=db,
        inspection_id=inspection_id,
        officer_id=current_user.id,
    )

    return ScanService.create_scan(
        db=db,
        inspection_id=inspection_id,
        data=data,
    )


@router.post(
    "/{inspection_id}/scans/{scan_id}/process",
)
def process_scan(
    inspection_id: int,
    scan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_officer),
):
    InspectionService.get_owned_inspection(
        db=db,
        inspection_id=inspection_id,
        officer_id=current_user.id,
    )

    scan = ScanService.get_scan(
        db=db,
        inspection_id=inspection_id,
        scan_id=scan_id,
    )

    # Prevent duplicate concurrent processing.
    if scan.status == "processing":
        raise HTTPException(
            status_code=409,
            detail="Scan is already being processed",
        )

    # Idempotent retry: return existing results for a completed scan.
    if scan.status == "completed":
        ocr_result = (
            db.query(OCRResult)
            .filter(OCRResult.scan_id == scan.id)
            .order_by(OCRResult.id.desc())
            .first()
        )

        declarations = (
            db.query(Declaration)
            .filter(Declaration.scan_id == scan.id)
            .order_by(Declaration.id.asc())
            .all()
        )

        # Repair an inconsistent completed scan if its OCR result is missing.
        if ocr_result is not None:
            compliance = ComplianceEvaluator.evaluate_inspection(
                db=db,
                inspection_id=inspection_id,
            )

            return {
                "scan_id": scan.id,
                "status": "completed",
                "ocr_result": {
                    "id": ocr_result.id,
                    "raw_text": ocr_result.raw_text,
                    "processing_ms": ocr_result.processing_ms,
                },
                "declarations": [
                    {
                        "id": declaration.id,
                        "field_name": declaration.field_name,
                        "value_text": declaration.value_text,
                        "normalized_value": declaration.normalized_value,
                        "numeric_value": (
                            float(declaration.numeric_value)
                            if declaration.numeric_value is not None
                            else None
                        ),
                        "unit": declaration.unit,
                        "extraction_method": declaration.extraction_method,
                    }
                    for declaration in declarations
                ],
                "compliance": compliance,
            }

        scan.status = "pending"
        scan.error_message = None
        scan.completed_at = None
        scan.processing_ms = None
        db.commit()

    # Failed scans can be retried cleanly.
    if scan.status == "failed":
        db.query(Declaration).filter(
            Declaration.scan_id == scan.id
        ).delete(synchronize_session=False)

        db.query(OCRResult).filter(
            OCRResult.scan_id == scan.id
        ).delete(synchronize_session=False)

        scan.status = "pending"
        scan.error_message = None
        scan.completed_at = None
        scan.processing_ms = None
        db.commit()

    try:
        ocr_result = OCRService.process_scan(
            db=db,
            scan_id=scan.id,
        )

        declarations = DeclarationExtractionService.extract_from_scan(
            db=db,
            scan_id=scan.id,
        )

        compliance = ComplianceEvaluator.evaluate_inspection(
            db=db,
            inspection_id=inspection_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return {
        "scan_id": scan.id,
        "status": "completed",
        "ocr_result": {
            "id": ocr_result.id,
            "raw_text": ocr_result.raw_text,
            "processing_ms": ocr_result.processing_ms,
        },
        "declarations": [
            {
                "id": declaration.id,
                "field_name": declaration.field_name,
                "value_text": declaration.value_text,
                "normalized_value": declaration.normalized_value,
                "numeric_value": (
                    float(declaration.numeric_value)
                    if declaration.numeric_value is not None
                    else None
                ),
                "unit": declaration.unit,
                "extraction_method": declaration.extraction_method,
            }
            for declaration in declarations
        ],
        "compliance": compliance,
    }
