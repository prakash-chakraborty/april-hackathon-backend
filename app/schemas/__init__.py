from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    created_at: Optional[datetime] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PageCreate(BaseModel):
    name: str

class PageUpdate(BaseModel):
    name: Optional[str] = None

class PageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None
    cards: list["CardResponse"] = []


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
    model_config = ConfigDict(from_attributes=True)

    id: int
    page_id: int
    created_by: Optional[int] = None
    title: str
    card_type: str
    metric_title: str
    metric_value: str
