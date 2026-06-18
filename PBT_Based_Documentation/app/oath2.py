"""oath2 handles the logic of creating, validing, and finding users via JWT token"""
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone 
import os 
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from schemas import TokenData
from database import get_db
from sqlalchemy.orm import Session
import models 

# Tells FastAPi where clients can obtain a token and makes token available
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
SECRET_KEY = os.getenv("JWT_KEY")
ALGORITHM = "HS256"
# The token should expire in 60 minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 60

"""
Need to create the JWT access token, verify the access token, and get the current user using the access token"""


def create_access_token(data:dict):
    """Function creates the JWT authentication token"""
    if not SECRET_KEY:
        raise RuntimeError("JWT_KEY environment variable not set")
    to_encode = data.copy()
    # Create the expiration time for when the key expires :D 
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Update the dictionary with expires
    to_encode.update({"exp":expire})
    # Encode the data via jwt
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)



def verify_access_token(token:str, credentials_exception):
    """function validates if the json token is valid"""
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        # The user_id is fed via the auth route
        id = payload.get("user_id")
        if not id:
            raise credentials_exception
        # ToenDa
        token_data = TokenData(id=id)
    # Token is not valid
    except JWTError:
        raise credentials_exception
    # if everything is valid, return the data TokenData(id=id)
    return token_data

def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    """Function makes fastapi look for authorization header, extracts the bearer token and passes the token string into token
    """
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"COULD NOT VALIDATE YOUR CREDENTIAL",
                                         headers={"WWW-Authenticate": "Bearer"})
    
    # Verify if the access token is correct or not , if valid then token = TokenData(id=id) 
    token = verify_access_token(token, credential_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user







