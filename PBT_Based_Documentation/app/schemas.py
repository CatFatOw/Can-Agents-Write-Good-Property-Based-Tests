from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime

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


class ModelProviderSelection(BaseModel):
    """Selected model/key provider for generation requests."""
    provider: str = "openai"
    api_key: str | None = None
    base_url: str | None = None
    model: str | None = None


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
    key_url: str | None = None
    requires_base_url: bool = False
    openai_compatible: bool = False
