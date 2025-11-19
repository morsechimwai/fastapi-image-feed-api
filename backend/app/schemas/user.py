"""User schemas."""
from uuid import UUID
from fastapi_users import schemas


class UserRead(schemas.BaseUser[UUID]):
    """User read schema."""
    pass


class UserCreate(schemas.BaseUserCreate):
    """User create schema."""
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """User update schema."""
    pass

