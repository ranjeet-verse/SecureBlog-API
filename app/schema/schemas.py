from pydantic import BaseModel, EmailStr, Field
from ..model.models import UserRole
from datetime import datetime
from typing import Optional



class TokenData(BaseModel):
    user_id: int
    role: UserRole

class CreateUser(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=64,  
        example="StrongPass123"
    )

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class UserResponse(BaseModel):
    user: UserOut
    access_token: str
    token_type: str

    model_config = {
        "from_attributes": True
    }


class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True

class UpdatePost(CreatePost):
    pass

class PatchPost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None


class PostResponse(CreatePost):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True