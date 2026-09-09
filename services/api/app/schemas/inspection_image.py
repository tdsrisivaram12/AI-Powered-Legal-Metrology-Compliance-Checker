from datetime import datetime

from pydantic import BaseModel, ConfigDict


class InspectionImageResponse(BaseModel):
    id: int
    inspection_id: int
    image_type: str
    storage_path: str
    original_filename: str | None
    mime_type: str | None
    sha256: str | None
    width: int | None
    height: int | None
    captured_at: datetime

    model_config = ConfigDict(from_attributes=True)