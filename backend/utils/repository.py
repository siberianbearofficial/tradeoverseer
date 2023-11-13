from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import insert, select, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, *args, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, session: AsyncSession, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.uuid)
        res = await session.execute(stmt)
        return res.scalar_one()

    async def edit_one(self, session: AsyncSession, uuid: UUID, data: dict) -> int:
        stmt = update(self.model).values(**data).filter_by(uuid=uuid).returning(self.model.uuid)
        res = await session.execute(stmt)
        return res.scalar_one()

    async def find_all(self, session, filter_dict: dict = None, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)

        if filter_dict:
            for key, val in filter_dict.items():
                if key in self.model.__dict__:
                    if val[0] == 'between':
                        stmt = stmt.filter(and_(self.model.__dict__[key] >= val[1],
                                                self.model.__dict__[key] <= val[2]))

        res = await session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res

    async def find_one(self, session, filter_dict: dict = None, **filter_by):
        stmt = select(self.model).filter_by(**filter_by).limit(2)
        res = await session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        if res:
            return res[0]
        else:
            return None

    async def delete_one(self, session, uuid: UUID):
        stmt = delete(self.model).where(self.model.uuid == uuid).returning(self.model.uuid)
        res = await session.execute(stmt)
        return res

    async def delete_all(self, session, filter_dict: dict = None, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by)
        res = await session.execute(stmt)
        return res
