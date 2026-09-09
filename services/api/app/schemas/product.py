from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    product_name: str
    brand_name: str | None = None
    category: str | None = None
    manufacturer_name: str | None = None
    manufacturer_address: str | None = None
    country_of_origin: str | None = None
    barcode: str | None = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    product_name: str | None = None
    brand_name: str | None = None
    category: str | None = None
    manufacturer_name: str | None = None
    manufacturer_address: str | None = None
    country_of_origin: str | None = None
    barcode: str | None = None


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)