"""User-account workflows independent of HTTP routing."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.repository import user_repository
from app.security import password


def register_user(db: Session, email: str, plain_password: str):
    if user_repository.get_user_by_email(db, email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"YOU CANNOT USE THE SAME EMAIL {email} TWICE")
    return user_repository.save(db, models.User(email=email, password=password.hash(plain_password)))


def register_admin(db: Session, email: str, plain_password: str):
    if user_repository.get_admin_by_email(db, email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"YOU CANNOT USE THE SAME EMAIL {email} TWICE")
    hashed_password = password.hash(plain_password)
    user = user_repository.get_user_by_email(db, email)
    if user is None:
        user = models.User(email=email, password=hashed_password)
        db.add(user)
    db.add(models.AdminUser(email=email, password=hashed_password))
    db.commit()
    db.refresh(user)
    return user


def change_password(db: Session, user: models.User, current_password: str, new_password: str):
    if not password.verify(current_password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Current password is incorrect.")
    if not new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password cannot be empty.")
    user.password = password.hash(new_password)
    return user_repository.save(db, user)


def delete_account(db: Session, user: models.User) -> None:
    user_repository.delete_user_with_documentation(db, user)


def get_user(db: Session, user_id: int):
    user = user_repository.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {user_id} not FOUND!")
    return user
