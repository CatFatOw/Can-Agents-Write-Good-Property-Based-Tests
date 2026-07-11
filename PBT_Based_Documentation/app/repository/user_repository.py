"""Persistence operations for users and administrator accounts."""

from sqlalchemy.orm import Session

from app import models


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_admin_by_email(db: Session, email: str):
    return db.query(models.AdminUser).filter(models.AdminUser.email == email).first()


def save(db: Session, entity):
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def delete_user_with_documentation(db: Session, user: models.User) -> None:
    db.query(models.Documentation).filter(
        models.Documentation.owner_id == user.id
    ).delete(synchronize_session=False)
    db.delete(user)
    db.commit()
