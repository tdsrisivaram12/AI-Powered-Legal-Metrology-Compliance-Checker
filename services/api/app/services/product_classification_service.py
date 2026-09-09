from sqlalchemy.orm import Session

from app.models.inspection import Inspection
from app.models.product import Product
from app.models.declaration import Declaration


class ProductClassificationService:

    @staticmethod
    def classify_inspection(
        db: Session,
        inspection_id: int,
    ) -> dict:

        inspection = db.get(Inspection, inspection_id)

        if inspection is None:
            raise ValueError("Inspection not found")

        product = None

        if inspection.product_id is not None:
            product = db.get(Product, inspection.product_id)

        declarations = (
            db.query(Declaration)
            .filter(Declaration.inspection_id == inspection_id)
            .order_by(Declaration.id)
            .all()
        )

        values = {
            declaration.field_name: declaration.value_text
            for declaration in declarations
        }

        product_name = (
            product.product_name
            if product is not None
            else None
        )

        category = (
            product.category
            if product is not None
            else None
        )

        manufacturer = values.get(
            "manufacturer_name"
        )

        quantity = values.get(
            "net_quantity"
        )

        classification = category or "unknown"

        return {
            "inspection_id": inspection_id,
            "product_id": inspection.product_id,
            "product_name": product_name,
            "category": classification,
            "manufacturer": manufacturer,
            "net_quantity": quantity,
            "classification_method": (
                "product_record"
                if category
                else "unknown"
            ),
        }
