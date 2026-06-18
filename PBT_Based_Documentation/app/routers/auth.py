"""Route handles the logic for user, jwt authentication and login endpoints"""
from fastapi import FastAPI, HTTPException, APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session 
import models
import database 
from database import get_db
import oath2 
from oath2 import get_current_user, verify_access_token
from schemas import Token
from utils import hash, verify


# Create the api router
router = APIRouter(prefix="/login", tags=["auth"])

# get the user, the output should follow the schemas Token
@router.post("/", response_model=Token)
# Oauth2password auto extracts login credentials, depends() basically calls another function before running the main functin under the dectorator
async def login(user_credential:OAuth2PasswordRequestForm=Depends(), db:Session = Depends(get_db)):
    # Get the user from the login credentials extracted via oauth2PasswordRequestForm
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
    
    # If the user doens't exist 
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"INVALID CREDENTIALS!")
    
    # If the user exists, verify if the provided credential is correct
    if not verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"INVALID CREDENTIALS")
    
    # If everything passes, create the JWT token for the user 
    access_token = oath2.create_access_token(data={"user_id":user.id})
    return {"access_token":access_token, "token_type":"bearer"}
    
    









