from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    brand_name: Mapped[str | None] = mapped_column(
        String(255)
    )

    category: Mapped[str | None] = mapped_column(
        String(100),
        index=True,
    )

    manufacturer_name: Mapped[str | None] = mapped_column(
        String(255)
    )

    manufacturer_address: Mapped[str | None] = mapped_column(
        String(1000)
    )

    country_of_origin: Mapped[str | None] = mapped_column(
        String(100)
    )

    barcode: Mapped[str | None] = mapped_column(
        String(100),
        unique=True,
        index=True,
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

    inspections: Mapped[list["Inspection"]] = relationship(
        back_populates="product"
    )