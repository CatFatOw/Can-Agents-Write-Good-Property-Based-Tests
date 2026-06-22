from database import Base 
from sqlalchemy import Column, Integer, ForeignKey, String, TIMESTAMP, Boolean, Text, Float, JSON
from datetime import datetime 
from sqlalchemy.sql.expression import text 
from sqlalchemy.dialects.postgresql import JSONB
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

    # Metrics for comparison
    ibd_doc_elo_rating = Column(Integer, nullable=False, server_default=text("1000"))
    td_doc_elo_rating = Column(Integer, nullable=False, server_default=text("1000"))

    # Metrics for bradely terry, which measures the probability that item A beats item B
    bt_ibd_rating = Column(Float, nullable=True)
    bt_td_rating = Column(Float, nullable=True)
    bt_ibd_win_prob = Column(Float, nullable=True)
    bt_ibd_win_prob_ci_lower = Column(Float, nullable=True)
    bt_ibd_win_prob_ci_upper = Column(Float, nullable=True)

    comparison_count = Column(Integer, nullable=False, server_default=text("0"))
    ibd_wins = Column(Integer, nullable=False, server_default=text("0"))
    td_wins = Column(Integer, nullable=False, server_default=text("0"))


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

class AdminUser(Base):
    """Creates the sql postgres database to store research/testers that are doing the study"""
    __tablename__ = "admin_user"
    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(Text, nullable=True)
    password = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text("now()"))
        

# We now need to create a table for the voting/area 
class Comparison(Base):
    __tablename__ = "comparison"
    id = Column(Integer, nullable=False, primary_key=True)

    documentation_id = Column(Integer, ForeignKey("documentation.id", ondelete="CASCADE"), nullable=False)
    winner = Column(String, nullable=False)  # "TD" or "IBD"

    comments = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    documentation = relationship("Documentation")
    user = relationship("User")

# Now create an assessment table used to store the assessments, questions, user responses etc
class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id = Column(Integer, primary_key=True)

    documentation_id = Column(
        Integer,
        ForeignKey("documentation.id", ondelete="CASCADE"),
        nullable=False
    )


    question = Column(Text, nullable=False)
    choices = Column(JSONB, nullable=True)
    correct_response = Column(Text, nullable=False)
    explanation = Column(Text, nullable=False)

    documentation = relationship("Documentation")

# each assessment attempts
class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"

    id = Column(Integer, primary_key=True)

    documentation_id = Column(Integer, ForeignKey("documentation.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    documentation_type = Column(String, nullable=False)

    total_questions = Column(Integer, nullable=False)
    total_correct = Column(Integer, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    documentation = relationship("Documentation")
    user = relationship("User")


class AssessmentRetakeGrant(Base):
    __tablename__ = "assessment_retake_grants"

    id = Column(Integer, primary_key=True)
    documentation_id = Column(Integer, ForeignKey("documentation.id", ondelete="CASCADE"), nullable=False)
    allow_all_users = Column(Boolean, nullable=False, server_default=text("false"))
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    user_email = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    documentation = relationship("Documentation")
    user = relationship("User", foreign_keys=[user_id])
    creator = relationship("User", foreign_keys=[created_by])
    
# User answers for each assessment
class AssessmentAnswer(Base):
    __tablename__ = "assessment_answers"

    id = Column(Integer, primary_key=True)

    attempt_id = Column(Integer, ForeignKey("assessment_attempts.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("assessment_questions.id", ondelete="CASCADE"), nullable=False)

    user_response = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    attempt = relationship("AssessmentAttempt")
    question = relationship("AssessmentQuestion")
    user = relationship("User")
