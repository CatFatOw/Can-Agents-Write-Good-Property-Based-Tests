"""This file handles with the user hashing and verification logic"""

from passlib.context import CryptContext

# Create a password hashing utility to hash the password into the database
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash(password:str):
    """Hashes plaintext password using bcrypt and returns the hashed password 
    
    CryptContext manages password hashing algorithms and allows:
    - Hashing passwords
    - Verifying passwords
    - Upgrading hashing algorithms later
    """
    return pwd_context.hash(password)

def verify(password:str, hashed_password:str):
    """Function verifies if a user provided password (password) is the same when hashed"""
    return pwd_context.verify(password, hashed_password)

