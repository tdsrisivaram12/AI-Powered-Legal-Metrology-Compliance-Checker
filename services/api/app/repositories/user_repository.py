from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:
        return db.get(User, user_id)

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        return db.scalar(
            select(User).where(User.email == email)
        )

    @staticmethod
    def list(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[User]:
        return list(
            db.scalars(
                select(User)
                .order_by(User.created_at.desc())
                .offset(skip)
                .limit(limit)
            ).all()
        )

    @staticmethod
    def create(
        db: Session,
        data: UserCreate,
        hashed_password: str,
    ) -> User:
        user = User(
            full_name=data.full_name,
            email=data.email,
            role_id=data.role_id,
            hashed_password=hashed_password,
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update(
        db: Session,
        user: User,
        data: UserUpdate,
    ) -> User:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user