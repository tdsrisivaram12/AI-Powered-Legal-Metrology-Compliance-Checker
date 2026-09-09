from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class VerificationCreate(BaseModel):
    decision: str = Field(
        pattern="^(PASS|REVIEW|REJECT)$"
    )
    remarks: str | None = None


class VerificationResponse(BaseModel):
    id: int
    inspection_id: int
    officer_id: int
    decision: str
    remarks: str | None
    verified_at: datetime

    model_config = ConfigDict(from_attributes=True)
