from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.scan import Scan
from app.schemas.scan import ScanCreate


class ScanRepository:
    @staticmethod
    def get_by_id(db: Session, scan_id: int) -> Scan | None:
        return db.get(Scan, scan_id)

    @staticmethod
    def list_by_inspection(
        db: Session,
        inspection_id: int,
    ) -> list[Scan]:
        return list(
            db.scalars(
                select(Scan)
                .where(Scan.inspection_id == inspection_id)
                .order_by(Scan.created_at.desc())
            ).all()
        )

    @staticmethod
    def create(db: Session, data: ScanCreate) -> Scan:
        scan = Scan(**data.model_dump())
        db.add(scan)
        db.commit()
        db.refresh(scan)
        return scan

    @staticmethod
    def update_status(
        db: Session,
        scan: Scan,
        status: str,
        error_message: str | None = None,
    ) -> Scan:
        scan.status = status
        scan.error_message = error_message
        db.commit()
        db.refresh(scan)
        return scan