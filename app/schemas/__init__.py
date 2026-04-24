from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PageCreate(BaseModel):
    name: str

class PageUpdate(BaseModel):
    name: Optional[str] = None

class PageResponse(BaseModel):
    id: int
    name: str
    created_at: Optional[datetime] = None
    cards: list["CardResponse"] = []

    class Config:
        from_attributes = True


class CardCreate(BaseModel):
    title: str
    card_type: str
    metric_title: str
    metric_value: str

class CardUpdate(BaseModel):
    title: Optional[str] = None
    card_type: Optional[str] = None
    metric_title: Optional[str] = None
    metric_value: Optional[str] = None

class CardResponse(BaseModel):
    id: int
    page_id: int
    title: str
    card_type: str
    metric_title: str
    metric_value: str

    class Config:
        from_attributes = True
