"""Authentication workflows backed by the user repository."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.repository import user_repository
from app.security import password


def authenticate_user(db: Session, email: str, plain_password: str):
    user = user_repository.get_user_by_email(db, email)
    if user is None or not password.verify(plain_password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="INVALID CREDENTIALS")
    return user


def authenticate_admin(db: Session, email: str, plain_password: str):
    admin = user_repository.get_admin_by_email(db, email)
    if admin is None or not password.verify(plain_password, admin.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="INVALID CREDENTIALS")

    user = user_repository.get_user_by_email(db, email)
    if user is None:
        user = user_repository.save(db, models.User(email=email, password=admin.password))
    return user
