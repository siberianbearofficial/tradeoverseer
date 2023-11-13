from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class InventoryItemRead(BaseModel):
    uuid: UUID
    user_uuid: UUID
    skin_uuid: UUID
    added_at: datetime
    price: str
    count: int

    class Config:
        from_attributes = True


class InventoryItemCreate(BaseModel):
    uuid: UUID
    user_uuid: UUID
    skin_uuid: UUID
    added_at: datetime
    price: str
    count: int


class InventoryItemUpdate(BaseModel):
    uuid: UUID
    user_uuid: UUID
    skin_uuid: UUID
    added_at: datetime
    price: str
    count: int
