"""Documentation workflows and authorization rules."""

import json

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.repository import documentation_repository as repository


def can_manage(documentation: models.Documentation, user: models.User, db: Session) -> bool:
    return documentation.owner_id == user.id or repository.is_admin(db, user.email)


def get_required(db: Session, documentation_id: int):
    documentation = repository.get_by_id(db, documentation_id)
    if documentation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"POST ID: {documentation_id} not found")
    return documentation


def get_manageable(db: Session, documentation_id: int, user: models.User):
    documentation = get_required(db, documentation_id)
    if not can_manage(documentation, user, db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return documentation


def list_visible(db: Session, user: models.User):
    return repository.list_all(db) if repository.is_admin(db, user.email) else repository.list_for_owner(db, user.id)


def create(db: Session, user: models.User, payload: dict):
    return repository.save(db, models.Documentation(owner_id=user.id, **payload))


def update(db: Session, documentation_id: int, user: models.User, payload: dict):
    documentation = get_manageable(db, documentation_id, user)
    for field, value in payload.items():
        setattr(documentation, field, value)
    return repository.save(db, documentation)


def update_invariants(db: Session, documentation_id: int, user: models.User, invariants):
    value = invariants if isinstance(invariants, str) else json.dumps(invariants)
    return update(db, documentation_id, user, {"invariants": value})


def update_traditional_markdown(db: Session, documentation_id: int, user: models.User, payload: dict):
    return update(db, documentation_id, user, {"TD_md": str(payload.get("TD_md") or payload.get("td_md") or "")})


def delete(db: Session, documentation_id: int, user: models.User) -> None:
    repository.delete(db, get_manageable(db, documentation_id, user))
