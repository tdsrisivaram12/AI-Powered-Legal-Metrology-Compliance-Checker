from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.declaration import Declaration
from app.models.user import User


router = APIRouter(
    prefix="/inspections",
    tags=["Declarations"],
)


@router.get("/{inspection_id}/declarations")
def list_declarations(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = (
        db.query(Declaration)
        .filter(
            Declaration.inspection_id == inspection_id
        )
        .order_by(Declaration.id)
        .all()
    )

    return [
        {
            "id": row.id,
            "inspection_id": row.inspection_id,
            "scan_id": row.scan_id,
            "image_id": row.image_id,
            "field_name": row.field_name,
            "value_text": row.value_text,
            "normalized_value": row.normalized_value,
            "numeric_value": (
                float(row.numeric_value)
                if row.numeric_value is not None
                else None
            ),
            "unit": row.unit,
            "confidence": (
                float(row.confidence)
                if row.confidence is not None
                else None
            ),
            "extraction_method": row.extraction_method,
            "bounding_box": row.bounding_box,
            "created_at": row.created_at,
        }
        for row in rows
    ]
