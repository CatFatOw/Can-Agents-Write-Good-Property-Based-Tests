from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os 

"""
Structure:
Database URL
engine to connect to the databse
Session ot talk to the database
Create base parent class
get_db function for future api_routes to make new sessions with the db"""

# # "postgresql://postgres:password@localhost/data_base_name"
# Set DATABASE_URL for Postgres. The sqlite fallback keeps local imports/tests
# from crashing before a developer has created their database.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ibd_local.db")
# Create engine to connect to the database
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Talk to the database 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the parent class (to create model tables)
Base = declarative_base()


def get_db():
    """Function creates a new database session. Extremely important for routes :D"""
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
