from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False
    created_at: datetime


class PostCreate(PostBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    user_id: int
    user_info: UserResponse
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int 


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


# pydantic model used in token endpoint for the response
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    upvote: bool
