from typing import Optional
from fastapi import HTTPException, status

from sqlmodel import Session, select, func
from pydantic import EmailStr

from app.models import User, UserPublic, UsersPublic, UserCreate
from app.auth.security import verify_password, get_password_hash

MAX_LIMIT = 100


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def get_users(self, skip: int = 0, limit: int = 100) -> UsersPublic:
        if skip < 0 or limit <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Skip and limit must be positive numbers.",
            )
        limit = min(limit, MAX_LIMIT)
        total = self.session.exec(select(func.count()).select_from(User)).one()
        users = self.session.exec(select(User).offset(skip).limit(limit)).all()
        return UsersPublic(data=users, count=total)

    def get_user_by_id(self, user_id: int) -> UserPublic:
        user = self._get_user_or_404(user_id)
        return user

    def create_user(self, user_data: UserCreate) -> UserPublic:
        email = user_data.email.lower()
        self._ensure_email_unique(email)

        if not user_data.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Password is required."
            )

        hashed_password = get_password_hash(user_data.password)

        new_user = User.model_validate(
            user_data, update={"hashed_password": hashed_password, "email": email}
        )

        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)

        return new_user

    def delete_user(self, user_id: int) -> dict:
        user = self._get_user_or_404(user_id)
        self.session.delete(user)
        self.session.commit()
        return {"detail": f"User with ID {user_id} deleted successfully."}

    def get_user_by_email_service(self, email: EmailStr) -> Optional[User]:
        return self.session.exec(
            select(User).where(User.email == email.lower())
        ).first()

    def authenticate_user_service(
        self, email: EmailStr, password: str
    ) -> Optional[User]:
        user = self.get_user_by_email_service(email=email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    # ---------- Private Methods ----------

    def _get_user_or_404(self, user_id: int) -> User:
        user = self.session.exec(select(User).where(User.id == user_id)).one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )
        return user

    def _ensure_email_unique(self, email: EmailStr):
        if self.get_user_by_email_service(email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already registered."
            )
