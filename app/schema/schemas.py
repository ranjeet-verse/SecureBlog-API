from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional
from ..model.models import UserRole
import bleach




class TokenData(BaseModel):
    user_id: int
    role: str   

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



class CreatePost(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    content: str = Field(min_length=10)
    published: bool = True

    @field_validator("title", "content")
    @classmethod
    def sanitize_text(cls, v: str):
        return bleach.clean(v, tags=[], strip=True)



class UpdatePost(CreatePost):
    pass

class PatchPost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

    @field_validator("title", "content")
    @classmethod
    def sanitize_text(cls, v: Optional[str]):
        if v is None:
            return v
        return bleach.clean(v, tags=[], strip=True)



class PostResponse(CreatePost):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True