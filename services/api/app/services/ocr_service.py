from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

import pytesseract
from PIL import Image
from sqlalchemy.orm import Session

from app.models.inspection_image import InspectionImage
from app.models.ocr_result import OCRResult
from app.models.scan import Scan


TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
STORAGE_ROOT = Path(__file__).resolve().parents[2] / "storage"


class OCRService:

    @staticmethod
    def process_scan(
        db: Session,
        scan_id: int,
    ) -> OCRResult:

        scan = db.get(Scan, scan_id)

        if scan is None:
            raise ValueError("Scan not found")

        if scan.image_id is None:
            raise ValueError("Scan has no image")

        image_record = db.get(
            InspectionImage,
            scan.image_id,
        )

        if image_record is None:
            raise ValueError("Inspection image not found")

        image_path = Path(image_record.storage_path)

        if not image_path.is_absolute():
            image_path = STORAGE_ROOT / image_path

        if not image_path.exists():
            raise ValueError(
                f"Image file not found: {image_path}"
            )

        pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

        scan.status = "processing"
        scan.error_message = None
        scan.started_at = scan.started_at or datetime.now(timezone.utc)

        db.commit()

        start = perf_counter()

        try:
            with Image.open(image_path) as image:
                text = pytesseract.image_to_string(
                    image,
                    lang="eng",
                    config="--psm 6",
                )

            processing_ms = int(
                (perf_counter() - start) * 1000
            )

            result = OCRResult(
                scan_id=scan.id,
                engine="tesseract",
                engine_version="5.5.3.20260724",
                language="eng",
                raw_text=text.strip(),
                confidence=None,
                processing_ms=processing_ms,
            )

            scan.status = "completed"
            scan.completed_at = datetime.now(timezone.utc)
            scan.processing_ms = processing_ms
            scan.pipeline_version = "ocr-v1"
            scan.error_message = None

            db.add(result)
            db.commit()
            db.refresh(result)

            return result

        except Exception as exc:
            processing_ms = int(
                (perf_counter() - start) * 1000
            )

            scan.status = "failed"
            scan.processing_ms = processing_ms
            scan.error_message = str(exc)
            scan.completed_at = datetime.now(timezone.utc)

            db.commit()

            raise ValueError(
                f"OCR processing failed: {exc}"
            ) from exc
