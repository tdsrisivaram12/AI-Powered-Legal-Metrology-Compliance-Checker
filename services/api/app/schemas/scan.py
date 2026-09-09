from pydantic import BaseModel, ConfigDict


class ScanCreate(BaseModel):
    image_id: int | None = None
    scan_type: str = "full"


class ScanResponse(BaseModel):
    id: int
    inspection_id: int
    image_id: int | None
    scan_type: str
    status: str
    pipeline_version: str | None
    error_message: str | None
    processing_ms: int | None
    started_at: object | None
    completed_at: object | None
    created_at: object
    updated_at: object

    model_config = ConfigDict(from_attributes=True)
