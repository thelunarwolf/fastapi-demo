import email
from typing import Optional
from pydantic import BaseModel

class Owner(BaseModel):
    id: int
    is_active: bool
    email: str
    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    description: Optional[str] = None


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    owner: Optional[Owner]
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    password: str

class UserLogin(UserUpdate):
    username: str

class User(UserBase):
    id: int
    is_active: bool
    items: list[Post] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None