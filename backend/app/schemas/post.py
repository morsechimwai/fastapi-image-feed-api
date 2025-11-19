"""Post schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl


class PostBase(BaseModel):
    """Base post schema."""
    caption: Optional[str] = None


class PostCreate(PostBase):
    """Post create schema."""
    pass


class PostRead(PostBase):
    """Post read schema."""
    id: str
    user_id: str
    url: HttpUrl
    file_id: Optional[str]
    file_type: str
    file_name: str
    created_at: datetime

    class Config:
        from_attributes = True


class PostInFeed(PostRead):
    """Post schema for feed display."""
    is_owner: bool
    email: str

