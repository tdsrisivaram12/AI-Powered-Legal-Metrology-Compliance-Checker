from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.inspection import Inspection
from app.models.inspection_image import InspectionImage
from app.models.scan import Scan
from app.schemas.scan import ScanCreate


class ScanService:

    @staticmethod
    def create_scan(
        db: Session,
        inspection_id: int,
        data: ScanCreate,
    ) -> Scan:

        inspection = db.get(Inspection, inspection_id)

        if inspection is None:
            raise HTTPException(
                status_code=404,
                detail="Inspection not found",
            )

        if data.image_id is not None:
            image = db.get(InspectionImage, data.image_id)

            if image is None or image.inspection_id != inspection_id:
                raise HTTPException(
                    status_code=404,
                    detail="Inspection image not found",
                )

        scan = Scan(
            inspection_id=inspection_id,
            image_id=data.image_id,
            scan_type=data.scan_type,
            status="pending",
        )

        db.add(scan)
        db.commit()
        db.refresh(scan)

        return scan

    @staticmethod
    def get_scan(
        db: Session,
        inspection_id: int,
        scan_id: int,
    ) -> Scan:

        scan = db.get(Scan, scan_id)

        if scan is None or scan.inspection_id != inspection_id:
            raise HTTPException(
                status_code=404,
                detail="Scan not found",
            )

        return scan
