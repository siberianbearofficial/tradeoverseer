from json import dumps
from uuid import UUID

from utils.unitofwork import IUnitOfWork
from utils.logic import hash_password

from .repository import UsersRepository
from .schemas import UserCreate, UserRead, UserUpdate, ChangePassword


class UsersService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    async def get_users(self, uow: IUnitOfWork, username: str | None = None, with_password: bool = False):
        async with uow:
            filter_by_dict = {'username': username} if username else {}
            if with_password:
                users = await self.users_repository.find_all_with_passwords(uow.session, **filter_by_dict)
            else:
                users = await self.users_repository.find_all(uow.session, **filter_by_dict)
            return users

    async def get_user(self, uow: IUnitOfWork, uuid: UUID, with_password: bool = False):
        async with uow:
            if with_password:
                user = await self.users_repository.find_one_with_password(uow.session, uuid=uuid)
            else:
                user = await self.users_repository.find_one(uow.session, uuid=uuid)
            return user

    async def add_user(self, uow: IUnitOfWork, user: UserCreate):
        async with uow:
            user_dict = {
                'uuid': user.uuid,
                'username': user.username,
                'subscribed_at': user.subscribed_at.replace(tzinfo=None),
                'roles': dumps(user.roles),
                'hashed_password': hash_password(user.password)
            }
            await self.users_repository.add_one(uow.session, user_dict)
            await uow.commit()

    async def update_user(self, uow: IUnitOfWork, user: UserUpdate, full_update: bool = False):
        if full_update:
            user_dict = {
                'username': user.username,
                'subscribed_at': user.subscribed_at.replace(tzinfo=None),
                'roles': dumps([str(role_uuid) for role_uuid in user.roles])
            }
        else:
            user_dict = {
                'username': user.username
            }
        async with uow:
            await self.users_repository.edit_one(uow.session, user.uuid, user_dict)
            await uow.commit()

    async def change_password(self, uow: IUnitOfWork, uuid: UUID, scheme: ChangePassword):
        async with uow:
            await self.users_repository.edit_one(uow.session, uuid, {
                'hashed_password': hash_password(scheme.new_password)
            })
            await uow.commit()

    async def delete_user(self, uow: IUnitOfWork, uuid: UUID):
        async with uow:
            await self.users_repository.delete_one(uow.session, uuid)
            await uow.commit()
