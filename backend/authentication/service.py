import jwt

from utils.unitofwork import IUnitOfWork
from utils.config import SECRET_AUTH

from users.service import UsersService


class AuthenticationService:
    def __init__(self, users_service: UsersService):
        self.users_service = users_service

    async def is_signed_in(self, uow: IUnitOfWork, authorization: str | None):
        if not authorization:
            return

        token = authorization.split()
        if len(token) <= 1:
            return

        token = token[1].strip()
        payload = jwt.decode(token, SECRET_AUTH, algorithms=['HS256'])
        uuid = payload['sub']

        if not uuid:
            return

        user = await self.users_service.get_user(uow, uuid)
        return user
