"""Persistence operations for generated documentation."""

from sqlalchemy.orm import Session

from app import models


def list_all(db: Session):
    return db.query(models.Documentation).all()


def list_for_owner(db: Session, owner_id: int):
    return db.query(models.Documentation).filter(models.Documentation.owner_id == owner_id).all()


def get_by_id(db: Session, documentation_id: int):
    return db.query(models.Documentation).filter(models.Documentation.id == documentation_id).first()


def get_owner_ibd(db: Session, owner_id: int):
    return db.query(models.Documentation.IBD_generated_md).filter(
        models.Documentation.owner_id == owner_id
    ).all()


def get_owner_td(db: Session, owner_id: int):
    return db.query(models.Documentation.TD_md).filter(models.Documentation.owner_id == owner_id).all()


def is_admin(db: Session, email: str) -> bool:
    return db.query(models.AdminUser).filter(models.AdminUser.email == email).first() is not None


def save(db: Session, documentation: models.Documentation):
    db.add(documentation)
    db.commit()
    db.refresh(documentation)
    return documentation


def delete(db: Session, documentation: models.Documentation) -> None:
    db.delete(documentation)
    db.commit()
