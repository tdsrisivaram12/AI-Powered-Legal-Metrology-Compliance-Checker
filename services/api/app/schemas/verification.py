from datetime import datetime

from pydantic import BaseModel, Field


class VerificationCreate(BaseModel):
    decision: str = Field(min_length=1, max_length=30)
    remarks: str | None = None


class VerificationResponse(BaseModel):
    id: int
    inspection_id: int
    officer_id: int
    decision: str
    remarks: str | None
    verified_at: datetime

    model_config = {"from_attributes": True}
