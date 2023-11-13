from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class UserRead(BaseModel):
    uuid: UUID
    username: str
    subscribed_at: datetime
    roles: list[UUID]

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    uuid: UUID
    username: str
    password: str
    subscribed_at: datetime
    roles: list[UUID]


class UserUpdate(BaseModel):
    uuid: UUID
    username: str
    subscribed_at: datetime
    roles: list[UUID]


class UserWithPassword(BaseModel):
    uuid: UUID
    username: str
    hashed_password: str
    subscribed_at: datetime
    roles: list[UUID]

    class Config:
        from_attributes = True


class ChangePassword(BaseModel):
    current_password: str
    new_password: str
