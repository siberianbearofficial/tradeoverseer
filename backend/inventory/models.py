from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Uuid, TIMESTAMP, String, Integer

from utils.database import Base

from users.models import User
from skins.models import Skin

from .schemas import InventoryItemRead


class InventoryItem(Base):
    __tablename__ = 'inventory'

    uuid = Column(Uuid, primary_key=True, default=uuid4)
    user_uuid = Column(Uuid, ForeignKey(User.uuid))
    skin_uuid = Column(Uuid, ForeignKey(Skin.uuid))
    added_at = Column(TIMESTAMP, default=datetime.utcnow)
    price = Column(String)
    count = Column(Integer)

    def to_read_model(self):
        return InventoryItemRead(
            uuid=self.uuid,
            user_uuid=self.user_uuid,
            skin_uuid=self.skin_uuid,
            added_at=self.added_at,
            price=self.price,
            count=self.count
        )
