from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class DeclarationCreate(BaseModel):
    inspection_id: int
    scan_id: int | None = None
    image_id: int | None = None

    field_name: str
    value_text: str | None = None
    normalized_value: str | None = None
    numeric_value: Decimal | None = None
    unit: str | None = None
    confidence: Decimal | None = None
    extraction_method: str | None = None
    bounding_box: dict | None = None


class DeclarationResponse(DeclarationCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)