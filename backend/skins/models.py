from uuid import uuid4
from sqlalchemy import (Column, String, Uuid, ForeignKey)
from utils.database import Base

from rarities.models import Rarity

from .schemas import SkinRead


class Skin(Base):
    __tablename__ = "skin"

    uuid = Column(Uuid, primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    rarity_uuid = Column(Uuid, ForeignKey(Rarity.uuid))

    def to_read_model(self) -> SkinRead:
        return SkinRead(
            uuid=self.uuid,
            name=self.name,
            rarity_uuid=self.rarity_uuid
        )
