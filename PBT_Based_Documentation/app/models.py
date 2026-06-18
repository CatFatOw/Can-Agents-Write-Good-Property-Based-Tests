from database import Base 
from sqlalchemy import Column, Integer, ForeignKey, String, TIMESTAMP, Boolean, Text, Float
from datetime import datetime 
from sqlalchemy.sql.expression import text 
from sqlalchemy.orm import relationship 


class Documentation(Base):
    """Creates the SQL postgres database to store the function api, md generated etc"""
    __tablename__ = "documentation"
    id = Column(Integer, nullable=False, primary_key=True)
    documentation_title = Column(Text, nullable=False)
    source_code = Column(Text,nullable=False)
    IBD_generated_md = Column(Text, nullable=False)
    TD_md = Column(Text, nullable=False)
    invariants = Column(Text, nullable=True)
    soundness = Column(Float)
    validity = Column(Float)
    mutation_score = Column(Float)
    mutation_summary = Column(Text)
    hypothesis_tests = Column(Text)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text("now()"))
    
    owner_id = Column(ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    owner = relationship("User")


class User(Base):
    """Creates the sql postgres databse to store the username/password of the users"""
    __tablename__ = "user"

    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
        
