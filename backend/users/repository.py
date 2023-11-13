from sqlalchemy import select, and_

from utils.repository import SQLAlchemyRepository

from .models import User


class UsersRepository(SQLAlchemyRepository):
    model = User

    async def find_all_with_passwords(self, session, filter_dict: dict = None, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)

        if filter_dict:
            for key, val in filter_dict.items():
                if key in self.model.__dict__:
                    if val[0] == 'between':
                        stmt = stmt.filter(and_(self.model.__dict__[key] >= val[1],
                                                self.model.__dict__[key] <= val[2]))

        res = await session.execute(stmt)
        res = [row[0].to_with_password_model() for row in res.all()]
        return res

    async def find_one_with_password(self, session, filter_dict: dict = None, **filter_by):
        stmt = select(self.model).filter_by(**filter_by).limit(2)
        res = await session.execute(stmt)
        res = [row[0].to_with_password_model() for row in res.all()]
        if res:
            return res[0]
        else:
            return None
