from uuid import uuid4
from datetime import datetime
from sqlalchemy import (TIMESTAMP, Column, ForeignKey, Integer, String, Uuid)
from utils.database import Base

from skins.models import Skin

from .schemas import RecordRead


class Record(Base):
    __tablename__ = "record"

    uuid = Column(Uuid, primary_key=True, default=uuid4)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    skin_uuid = Column(Uuid, ForeignKey(Skin.uuid))
    price = Column(String, nullable=False)
    count = Column(Integer, nullable=False)

    def to_read_model(self) -> RecordRead:
        return RecordRead(
            uuid=self.uuid,
            registered_at=self.registered_at,
            skin_uuid=self.skin_uuid,
            price=self.price,
            count=self.count
        )
