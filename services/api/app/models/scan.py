from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Scan(Base):
    __tablename__ = "scans"

    id: Mapped[int] = mapped_column(primary_key=True)

    inspection_id: Mapped[int] = mapped_column(
        ForeignKey("inspections.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    image_id: Mapped[int | None] = mapped_column(
        ForeignKey("inspection_images.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    scan_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="full",
        server_default="full",
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="pending",
        server_default="pending",
        index=True,
    )

    pipeline_version: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    processing_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    inspection: Mapped["Inspection"] = relationship(
        back_populates="scans",
    )

    image: Mapped["InspectionImage | None"] = relationship(
        back_populates="scans",
    )

    ocr_results: Mapped[list["OCRResult"]] = relationship(
        back_populates="scan",
        cascade="all, delete-orphan",
    )

    declarations: Mapped[list["Declaration"]] = relationship(
        back_populates="scan",
        cascade="all, delete-orphan",
    )