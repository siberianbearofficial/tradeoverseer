from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class RecordRead(BaseModel):
    uuid: UUID
    registered_at: datetime
    skin_uuid: UUID
    price: str
    count: int

    class Config:
        from_attributes = True


class RecordCreate(BaseModel):
    uuid: UUID | None
    registered_at: datetime | None
    skin_uuid: UUID
    price: str
    count: int

    class Config:
        from_attributes = True


class RecordUpdate(BaseModel):
    uuid: UUID
    registered_at: datetime
    skin_uuid: UUID
    price: str
    count: int
