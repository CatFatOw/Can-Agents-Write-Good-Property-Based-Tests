"""This file handles the routing for users, such as creating users, and getting a specific user with an ID"""
from fastapi import APIRouter, Depends, status, HTTPException, Response
import models
import database
from database import get_db
from schemas import UserModel, UserResponse, PasswordChange
import utils, oath2
from sqlalchemy.orm import Session
import admin

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user:UserModel, db:Session = Depends(get_db)):
    """Function creates an user"""
    curr_user = db.query(models.User).filter(models.User.email == user.email).first()
    if curr_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"YOU CANNOT USE THE SAME EMAIL {user.email} TWICE")
    # If the user doesn't exist 
    hashed_password = utils.hash(user.password)
    # update the user's password to the hashed password
    user.password = hashed_password
    
    # now add/update the user to the DB table!
    new_user = models.User(**user.model_dump())
    # Add the new user to the db
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/admin", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_admin_user(user: UserModel, db: Session = Depends(get_db)):
    """Create an admin account and ensure it can authenticate through JWT."""
    admin_user = db.query(models.AdminUser).filter(models.AdminUser.email == user.email).first()
    if admin_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"YOU CANNOT USE THE SAME EMAIL {user.email} TWICE")

    hashed_password = utils.hash(user.password)
    curr_user = db.query(models.User).filter(models.User.email == user.email).first()
    if curr_user is None:
        curr_user = models.User(email=user.email, password=hashed_password)
        db.add(curr_user)
    new_admin = models.AdminUser(email=user.email, password=hashed_password)
    db.add(new_admin)
    db.commit()
    db.refresh(curr_user)
    return curr_user



    

# CURRENT USER (ACCOUNT) ENDPOINT LOGIC START----
@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(curr_user: models.User = Depends(oath2.get_current_user)):
    """Return the profile (name/email, created time) for the logged-in user."""
    return curr_user

@router.get("/me/admin", response_model=UserResponse)
async def get_current_admin_profile(curr_admin: models.AdminUser = Depends(admin.get_current_admin)):
    """Return the profile for the logged-in admin user."""
    return curr_admin


@router.put("/me/password", response_model=UserResponse)
async def change_password(
    payload: PasswordChange,
    db: Session = Depends(get_db),
    curr_user: models.User = Depends(oath2.get_current_user),
):
    """Let the logged-in user change their own password."""
    if not utils.verify(payload.current_password, curr_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Current password is incorrect.",
        )
    if not payload.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password cannot be empty.",
        )
    curr_user.password = utils.hash(payload.new_password)
    db.commit()
    db.refresh(curr_user)
    return curr_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(
    db: Session = Depends(get_db),
    curr_user: models.User = Depends(oath2.get_current_user),
):
    """Delete the logged-in user's account along with all their documentation."""
    # Remove owned documentation first so the delete works even when the
    # database (e.g. SQLite) does not enforce the ON DELETE CASCADE foreign key.
    db.query(models.Documentation).filter(
        models.Documentation.owner_id == curr_user.id
    ).delete(synchronize_session=False)
    db.delete(curr_user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
# CURRENT USER (ACCOUNT) ENDPOINT LOGIC END----


@router.get("/{id}", response_model=UserResponse)
async def get_user(id:int, db:Session = Depends(get_db)):
    """route to get a specific user id :D"""
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {id} not FOUND!")
    return user





