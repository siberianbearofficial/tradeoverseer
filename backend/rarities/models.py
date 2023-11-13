from uuid import uuid4
from sqlalchemy import (Column, String, Uuid)
from utils.database import Base

from .schemas import RarityRead


class Rarity(Base):
    __tablename__ = "rarity"

    uuid = Column(Uuid, primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)

    def to_read_model(self) -> RarityRead:
        return RarityRead(
            uuid=self.uuid,
            name=self.name,
            color=self.color
        )
