from hashlib import sha256

from sqlalchemy.orm import Session

from app.models.declaration import Declaration
from app.models.inspection_image import InspectionImage


class EvidenceService:

    @staticmethod
    def get_inspection_evidence(
        db: Session,
        inspection_id: int,
    ) -> dict:

        images = (
            db.query(InspectionImage)
            .filter(
                InspectionImage.inspection_id == inspection_id
            )
            .order_by(InspectionImage.id)
            .all()
        )

        declarations = (
            db.query(Declaration)
            .filter(
                Declaration.inspection_id == inspection_id
            )
            .order_by(Declaration.id)
            .all()
        )

        evidence = []

        for image in images:
            image_declarations = [
                {
                    "id": d.id,
                    "field_name": d.field_name,
                    "value": d.value_text,
                    "extraction_method": d.extraction_method,
                    "confidence": (
                        float(d.confidence)
                        if d.confidence is not None
                        else None
                    ),
                    "bounding_box": d.bounding_box,
                }
                for d in declarations
                if d.image_id == image.id
            ]

            evidence.append(
                {
                    "image_id": image.id,
                    "inspection_id": image.inspection_id,
                    "original_filename": image.original_filename,
                    "storage_path": image.storage_path,
                    "mime_type": image.mime_type,
                    "sha256": image.sha256,
                    "integrity_verified": (
                        image.sha256 is not None
                        and len(image.sha256) == 64
                    ),
                    "declarations": image_declarations,
                }
            )

        return {
            "inspection_id": inspection_id,
            "image_count": len(images),
            "evidence": evidence,
        }
