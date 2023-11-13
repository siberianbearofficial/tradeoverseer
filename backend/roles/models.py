from uuid import uuid4
from json import loads

from sqlalchemy import Column, String, Uuid

from utils.database import Base

from .schemas import RoleRead


class Role(Base):
    __tablename__ = 'role'

    uuid = Column(Uuid, primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    permissions = Column(String)

    def to_read_model(self):
        return RoleRead(
            uuid=self.uuid,
            name=self.name,
            permissions=loads(self.permissions)
        )
