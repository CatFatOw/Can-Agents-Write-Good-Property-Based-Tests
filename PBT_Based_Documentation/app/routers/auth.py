"""Route handles the logic for user, jwt authentication and login endpoints"""
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from app.database import get_db
from app.security import oauth2
from app.schemas import Token
from app.services import auth_service


# Create the api router
router = APIRouter(prefix="/login", tags=["auth"])

# get the user, the output should follow the schemas Token
@router.post("/", response_model=Token)
# Oauth2password auto extracts login credentials, depends() basically calls another function before running the main functin under the dectorator
async def login(user_credential:OAuth2PasswordRequestForm=Depends(), db:Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, user_credential.username, user_credential.password)
    access_token = oauth2.create_access_token(data={"user_id":user.id})
    return {"access_token":access_token, "token_type":"bearer"}
    

@router.post("/admin", response_model=Token)
async def login_admin(user_credential:OAuth2PasswordRequestForm=Depends(), db:Session = Depends(get_db)):
    """function logs in the admin"""
    user = auth_service.authenticate_admin(db, user_credential.username, user_credential.password)
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
