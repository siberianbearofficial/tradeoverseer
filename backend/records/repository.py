from sqlalchemy import select

from utils.repository import SQLAlchemyRepository

from .models import Record


class RecordsRepository(SQLAlchemyRepository):
    model = Record

    async def find_latest(self, session, filter_dict: dict = None, **filter_by):
        stmt = select(self.model).filter_by(**filter_by).order_by(self.model.registered_at.desc()).limit(2)
        res = await session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        if res:
            return res[0]
        else:
            return None
