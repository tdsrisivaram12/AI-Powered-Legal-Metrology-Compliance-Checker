from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.declaration import Declaration
from app.schemas.declaration import DeclarationCreate


class DeclarationRepository:
    @staticmethod
    def get_by_id(
        db: Session,
        declaration_id: int,
    ) -> Declaration | None:
        return db.get(Declaration, declaration_id)

    @staticmethod
    def list_by_inspection(
        db: Session,
        inspection_id: int,
    ) -> list[Declaration]:
        return list(
            db.scalars(
                select(Declaration)
                .where(
                    Declaration.inspection_id == inspection_id
                )
                .order_by(Declaration.created_at.asc())
            ).all()
        )

    @staticmethod
    def create(
        db: Session,
        data: DeclarationCreate,
    ) -> Declaration:
        declaration = Declaration(**data.model_dump())
        db.add(declaration)
        db.commit()
        db.refresh(declaration)
        return declaration

    @staticmethod
    def create_many(
        db: Session,
        declarations: list[DeclarationCreate],
    ) -> list[Declaration]:
        objects = [
            Declaration(**item.model_dump())
            for item in declarations
        ]

        db.add_all(objects)
        db.commit()

        for obj in objects:
            db.refresh(obj)

        return objects