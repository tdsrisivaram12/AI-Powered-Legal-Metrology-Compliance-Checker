from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ocr_result import OCRResult
from app.schemas.ocr_result import OCRResultCreate


class OCRResultRepository:
    @staticmethod
    def get_by_id(db: Session, ocr_result_id: int) -> OCRResult | None:
        return db.get(OCRResult, ocr_result_id)

    @staticmethod
    def list_by_scan(
        db: Session,
        scan_id: int,
    ) -> list[OCRResult]:
        return list(
            db.scalars(
                select(OCRResult)
                .where(OCRResult.scan_id == scan_id)
                .order_by(OCRResult.created_at.desc())
            ).all()
        )

    @staticmethod
    def create(
        db: Session,
        data: OCRResultCreate,
    ) -> OCRResult:
        result = OCRResult(**data.model_dump())
        db.add(result)
        db.commit()
        db.refresh(result)
        return result