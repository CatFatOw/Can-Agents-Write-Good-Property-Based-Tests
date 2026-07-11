"""This file handles the routing for users, such as creating users, and getting a specific user with an ID"""
from fastapi import APIRouter, Depends, status, HTTPException, Response, BackgroundTasks
from app.database import get_db
from app.schemas import UserModel, UserResponse, PasswordChange
from app.security import admin, oauth2
from app.services import user_service
from app import models
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user:UserModel, db:Session = Depends(get_db)):
    """Function creates an user"""
    return user_service.register_user(db, user.email, user.password)


@router.post("/admin", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_admin_user(user: UserModel, db: Session = Depends(get_db)):
    """Create an admin account and ensure it can authenticate through JWT."""
    return user_service.register_admin(db, user.email, user.password)



    

# CURRENT USER (ACCOUNT) ENDPOINT LOGIC START----
@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(curr_user: models.User = Depends(oauth2.get_current_user)):
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
    curr_user: models.User = Depends(oauth2.get_current_user),
):
    """Let the logged-in user change their own password."""
    return user_service.change_password(db, curr_user, payload.current_password, payload.new_password)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(
    db: Session = Depends(get_db),
    curr_user: models.User = Depends(oauth2.get_current_user),
):
    """Delete the logged-in user's account along with all their documentation."""
    user_service.delete_account(db, curr_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
# CURRENT USER (ACCOUNT) ENDPOINT LOGIC END----


@router.get("/{id}", response_model=UserResponse)
async def get_user(id:int, db:Session = Depends(get_db)):
    """route to get a specific user id :D"""
    return user_service.get_user(db, id)

