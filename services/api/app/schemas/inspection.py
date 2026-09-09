from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


INSPECTION_STATUSES = (
    "draft",
    "in_progress",
    "review",
    "completed",
    "closed",
)


class InspectionCreate(BaseModel):
    inspection_number: str
    product_id: int | None = None
    status: str = Field(
        default="draft",
        pattern="^(draft|in_progress|review|completed|closed)$",
    )
    notes: str | None = None


class InspectionUpdate(BaseModel):
    product_id: int | None = None
    status: str | None = Field(
        default=None,
        pattern="^(draft|in_progress|review|completed|closed)$",
    )
    notes: str | None = None


class InspectionResponse(BaseModel):
    id: int
    inspection_number: str
    officer_id: int
    product_id: int | None
    status: str
    notes: str | None
    started_at: datetime
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
