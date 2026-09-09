from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class OCRResultCreate(BaseModel):
    scan_id: int
    engine: str
    engine_version: str | None = None
    language: str | None = None
    raw_text: str
    confidence: Decimal | None = None
    processing_ms: int | None = None


class OCRResultResponse(OCRResultCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)