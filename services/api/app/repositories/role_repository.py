from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role import Role
from app.schemas.role import RoleCreate


class RoleRepository:
    @staticmethod
    def get_by_id(db: Session, role_id: int) -> Role | None:
        return db.get(Role, role_id)

    @staticmethod
    def get_by_name(db: Session, name: str) -> Role | None:
        return db.scalar(
            select(Role).where(Role.name == name)
        )

    @staticmethod
    def create(db: Session, data: RoleCreate) -> Role:
        role = Role(**data.model_dump())
        db.add(role)
        db.commit()
        db.refresh(role)
        return role