from uuid import uuid4
from datetime import datetime
from json import loads

from sqlalchemy import TIMESTAMP, Column, String, Uuid

from utils.database import Base

from .schemas import UserRead, UserWithPassword


class User(Base):
    __tablename__ = 'user'

    uuid = Column(Uuid, primary_key=True, default=uuid4)
    username = Column(String, nullable=False)
    subscribed_at = Column(TIMESTAMP, default=datetime.utcnow)
    roles = Column(String)
    hashed_password: str = Column(String(length=1024), nullable=False)

    def to_read_model(self):
        return UserRead(
            uuid=self.uuid,
            username=self.username,
            subscribed_at=self.subscribed_at,
            roles=loads(self.roles)
        )

    def to_with_password_model(self):
        return UserWithPassword(
            uuid=self.uuid,
            username=self.username,
            hashed_password=self.hashed_password,
            subscribed_at=self.subscribed_at,
            roles=loads(self.roles)
        )
