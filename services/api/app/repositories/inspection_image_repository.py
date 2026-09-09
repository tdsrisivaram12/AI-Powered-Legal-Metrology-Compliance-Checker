from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inspection_image import InspectionImage


class InspectionImageRepository:
    @staticmethod
    def get_by_id(
        db: Session,
        image_id: int,
    ) -> InspectionImage | None:
        return db.get(InspectionImage, image_id)

    @staticmethod
    def list_by_inspection(
        db: Session,
        inspection_id: int,
    ) -> list[InspectionImage]:
        return list(
            db.scalars(
                select(InspectionImage)
                .where(
                    InspectionImage.inspection_id == inspection_id
                )
                .order_by(InspectionImage.captured_at.asc())
            ).all()
        )

    @staticmethod
    def create(
        db: Session,
        image: InspectionImage,
    ) -> InspectionImage:
        db.add(image)
        db.commit()
        db.refresh(image)
        return image