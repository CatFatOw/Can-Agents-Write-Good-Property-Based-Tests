"""This file handles the routing for users, such as creating users, and getting a specific user with an ID"""
from fastapi import APIRouter, Depends, status, HTTPException
import models 
import database 
from database import get_db 
from schemas import UserModel, UserResponse
import utils, oath2 
from sqlalchemy.orm import Session

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

@router.get("/{id}", response_model=UserResponse)
async def get_user(id:int, db:Session = Depends(get_db)):
    """route to get a specific user id :D"""
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {id} not FOUND!")
    return user






