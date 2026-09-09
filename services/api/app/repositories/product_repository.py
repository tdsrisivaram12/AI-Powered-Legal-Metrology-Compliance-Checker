from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductRepository:
    @staticmethod
    def get_by_id(db: Session, product_id: int) -> Product | None:
        return db.get(Product, product_id)

    @staticmethod
    def get_by_barcode(db: Session, barcode: str) -> Product | None:
        return db.scalar(
            select(Product).where(Product.barcode == barcode)
        )

    @staticmethod
    def list(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Product]:
        return list(
            db.scalars(
                select(Product)
                .offset(skip)
                .limit(limit)
            ).all()
        )

    @staticmethod
    def create(db: Session, data: ProductCreate) -> Product:
        product = Product(**data.model_dump())
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def update(
        db: Session,
        product: Product,
        data: ProductUpdate,
    ) -> Product:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)

        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def delete(db: Session, product: Product) -> None:
        db.delete(product)
        db.commit()