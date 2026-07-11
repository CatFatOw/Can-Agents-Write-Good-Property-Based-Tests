from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session 
from app import models
from app.database import get_db
from app.security import oauth2


def get_current_admin(db:Session = Depends(get_db), curr_user:Session = Depends(oauth2.get_current_user)):
    """Function gets/valididates if the current user is in the admin database """
    admin = db.query(models.AdminUser).filter(models.AdminUser.email==curr_user.email).first()

    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=F"ONLY ADMIN USERS ARE ALLOWED")

    return admin
