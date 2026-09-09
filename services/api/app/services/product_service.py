from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:

    @staticmethod
    def create_product(db: Session, data: ProductCreate) -> Product:
        if data.barcode:
            existing = ProductRepository.get_by_barcode(db, data.barcode)

            if existing:
                raise HTTPException(
                    status_code=409,
                    detail="Product with this barcode already exists",
                )

        return ProductRepository.create(db, data)

    @staticmethod
    def get_product(db: Session, product_id: int) -> Product:
        product = ProductRepository.get_by_id(db, product_id)

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        return product

    @staticmethod
    def list_products(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Product]:

        if skip < 0:
            raise HTTPException(
                status_code=400,
                detail="skip must be >= 0",
            )

        if limit < 1 or limit > 100:
            raise HTTPException(
                status_code=400,
                detail="limit must be between 1 and 100",
            )

        return ProductRepository.list(
            db,
            skip=skip,
            limit=limit,
        )

    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        data: ProductUpdate,
    ) -> Product:

        product = ProductService.get_product(db, product_id)

        if data.barcode:
            existing = ProductRepository.get_by_barcode(
                db,
                data.barcode,
            )

            if existing and existing.id != product_id:
                raise HTTPException(
                    status_code=409,
                    detail="Product with this barcode already exists",
                )

        return ProductRepository.update(
            db,
            product,
            data,
        )
