from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    ForeignKey,
    JSON,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Declaration(Base):
    __tablename__ = "declarations"

    id: Mapped[int] = mapped_column(primary_key=True)

    inspection_id: Mapped[int] = mapped_column(
        ForeignKey("inspections.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    scan_id: Mapped[int | None] = mapped_column(
        ForeignKey("scans.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    image_id: Mapped[int | None] = mapped_column(
        ForeignKey("inspection_images.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    field_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    value_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    normalized_value: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    numeric_value: Mapped[Decimal | None] = mapped_column(
        Numeric(14, 4),
        nullable=True,
    )

    unit: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    confidence: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 4),
        nullable=True,
    )

    extraction_method: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    bounding_box: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    scan: Mapped["Scan | None"] = relationship(
        back_populates="declarations",
    )