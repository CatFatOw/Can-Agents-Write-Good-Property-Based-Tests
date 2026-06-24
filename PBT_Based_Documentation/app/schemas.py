from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime
from typing import Literal, List, Dict

# --------------------------INPUT MODELS----------------------
# Documentation
class Documentation(BaseModel):
    documentation_title: str
    source_code: str
    IBD_generated_md: str
    TD_md: str
    invariants: str | None = None
    soundness: float | None = None
    validity: float | None = None
    mutation_score: float | None = None
    mutation_summary: str | None = None
    hypothesis_tests: str | None = None


class InvariantsUpdate(BaseModel):
    """Payload for updating saved invariants without replacing the whole doc."""
    invariants: str | list[Any] | dict[str, Any]

# Create the oath2 scheme
class TokenData(BaseModel):
    id:Optional[int] = None

# Users
class UserModel(BaseModel):
    email:str
    password:str


class PasswordChange(BaseModel):
    """Payload for a logged-in user changing their own password."""
    current_password: str
    new_password: str


class ModelProviderSelection(BaseModel):
    """Selected model/key provider for generation requests."""
    provider: str = "openai"
    api_key: str | None = None
    base_url: str | None = None
    model: str | None = None

class ComparisonRequest(BaseModel):
    documentation_id:int
    winner: Literal["TD", "IBD"]
    comments:str

# Assessment submission schema
class AssessmentSubmit(BaseModel):
    attempt_id: int
    question_id: int
    user_response: str
    user_id:int


class AssessmentQuestionSubmit(BaseModel):
    id:int
    documentation_id:int
    question:str
    choices: dict
    correct_response: str
    explanation: str

# --------------------------RESPONSE MODELS--------------------

# Documentation
class DocumentationResponse(BaseModel):
    id: int
    documentation_title: str
    source_code: str
    IBD_generated_md: str
    TD_md: str
    invariants: str| None = None
    hypothesis_tests: str | None = None

    soundness: float | None = None
    validity: float | None = None
    mutation_score: float | None = None
    mutation_summary: str | None = None

    ibd_doc_elo_rating: int | None = None
    td_doc_elo_rating: int | None = None
    bt_ibd_rating: float | None = None
    bt_td_rating: float | None = None
    bt_ibd_win_prob: float | None = None
    bt_ibd_win_prob_ci_lower: float | None = None
    bt_ibd_win_prob_ci_upper: float | None = None
    comparison_count: int = 0
    ibd_wins: int = 0
    td_wins: int = 0
    question_count: int = 0
    response_count: int = 0

    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserIBDResponse(BaseModel):
    user_ibd: list[str]

class UserTDResponse(BaseModel):
    user_td: list[str]

class PostIBDResponse(BaseModel):
    post_IBD: str | None = None

class PostTDResponse(BaseModel):
    post_TD: str | None = None
# auth
class Token(BaseModel):
    access_token:str
    token_type:str

# User
class UserResponse(BaseModel):
    id:int
    email:str
    created_at:datetime

    class Config:
        from_attributes = True


class ModelProviderResponse(BaseModel):
    id: str
    label: str
    key_label: str
    key_placeholder: str
    default_model: str | None = None
    default_markdown_model: str | None = None
    default_metrics_model: str | None = None
    key_url: str | None = None
    requires_base_url: bool = False
    openai_compatible: bool = False

# Comparison

class RandomComparisonResponse(BaseModel):
    documentation_id: int
    documentation_title: str

    td_doc: str
    ibd_doc: str

    # Elo
    ibd_doc_elo_rating: int
    td_doc_elo_rating: int

    # Bradley-Terry
    bt_ibd_rating: Optional[float] = None
    bt_td_rating: Optional[float] = None
    bt_ibd_win_prob: Optional[float] = None
    bt_ibd_win_prob_ci_lower: Optional[float] = None
    bt_ibd_win_prob_ci_upper: Optional[float] = None
    bt_ibd_win_prob_ci_lower: Optional[float] = None

    # Research Statistics
    comparison_count: int = 0
    IBD_wins: int = 0
    TD_wins: int = 0

    # Percentages
    IBD_win_percentage: float = 0
    TD_win_percentage: float = 0

    created_at: datetime


class ComparisonResponse(BaseModel):
    id: int
    documentation_id: int
    winner: Literal["TD", "IBD"]

    # Elo
    ibd_doc_elo_rating: int
    td_doc_elo_rating: int

    # Bradley-Terry
    bt_ibd_rating: Optional[float] = None
    bt_td_rating: Optional[float] = None
    bt_ibd_win_prob: Optional[float] = None
    bt_ibd_win_prob_ci_lower: Optional[float] = None
    bt_ibd_win_prob_ci_upper: Optional[float] = None

    # Research Statistics
    comparison_count: int = 0
    IBD_wins: int = 0
    TD_wins: int = 0

    # Percentages
    IBD_win_percentage: float = 0
    TD_win_percentage: float = 0

    comments: str
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True



class AssessmentQuestionResponse(BaseModel):
    id: int
    question: str
    choices: Dict[str, str]


class AssessmentQuestionAdminResponse(BaseModel):
    id: int
    documentation_id: int
    question: str
    choices: Dict[str, str]
    correct_response: str
    explanation: str

    class Config:
        orm_mode = True


class AssessmentQuestionUpdate(BaseModel):
    question: str
    choices: Dict[str, str]
    correct_response: str
    explanation: str


class AssessmentAnswerAdminResponse(BaseModel):
    id: int
    attempt_id: int
    question_id: int
    documentation_id: int
    user_id: int
    user_email: str | None = None
    user_response: str
    is_correct: bool


class AssessmentRetakeGrantRequest(BaseModel):
    scope: Literal["all", "user"] = "all"
    user_id: int | None = None
    user_email: str | None = None


class AssessmentRetakeGrantResponse(BaseModel):
    id: int
    documentation_id: int
    allow_all_users: bool
    user_id: int | None = None
    user_email: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class AssessmentDocumentationOption(BaseModel):
    documentation_id: int
    documentation_title: str
    question_count: int
    response_count: int = 0
    attempted: bool = False


class AssessmentResponse(BaseModel):
    attempt_id: int
    documentation_id: int
    documentation_title: str
    documentation_type: str
    documentation: str
    questions: List[AssessmentQuestionResponse]

# Schema for user submission
class AssessmentAnswerResponse(BaseModel):
    id: int
    attempt_id: int
    question_id: int
    user_response: str
    is_correct: bool
    correct_response: str
    explanation: str

    class Config:
        orm_mode=True

# Schema for user stats
class AssessmentStatsResponse(BaseModel):
    total_answered: int
    total_correct: int
    total_incorrect: int
    percentage_correct: float
