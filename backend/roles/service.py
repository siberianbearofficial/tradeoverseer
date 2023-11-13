from typing import Iterable
from uuid import UUID
from json import dumps

from utils.unitofwork import IUnitOfWork

from users.schemas import UserRead, UserCreate, UserUpdate

from .repository import RolesRepository
from .schemas import RoleCreate, RoleUpdate


class RolesService:
    def __init__(self, roles_repository: RolesRepository):
        self.roles_repository = roles_repository

    async def get_roles(self, uow: IUnitOfWork, name: str | None = None):
        filter_by = {'name': name} if name else {}
        async with uow:
            roles = await self.roles_repository.find_all(uow.session, **filter_by)
            return roles

    async def get_role(self, uow: IUnitOfWork, uuid: UUID):
        async with uow:
            role = await self.roles_repository.find_one(uow.session, uuid=uuid)
            return role

    async def add_role(self, uow: IUnitOfWork, role: RoleCreate):
        async with uow:
            role_dict = {
                'uuid': role.uuid,
                'name': role.name,
                'permissions': dumps(role.permissions)
            }
            await self.roles_repository.add_one(uow.session, role_dict)
            await uow.commit()

    async def update_role(self, uow: IUnitOfWork, role: RoleUpdate):
        async with uow:
            role_dict = {
                'name': role.name,
                'permissions': dumps(role.permissions)
            }
            await self.roles_repository.edit_one(uow.session, role.uuid, role_dict)
            await uow.commit()

    async def delete_role(self, uow: IUnitOfWork, uuid: UUID):
        async with uow:
            await self.roles_repository.delete_one(uow.session, uuid)
            await uow.commit()

    async def delete_roles(self, uow: IUnitOfWork, name: str | None = None):
        filter_by_dict = {'name': name} if name else {}
        async with uow:
            await self.roles_repository.delete_all(uow.session, **filter_by_dict)
            await uow.commit()

    async def get_fake_role(self, uow: IUnitOfWork, roles: Iterable) -> str | None:
        """
        Function that returns uuid of the first role from the given list that does not exist.
        :param roles: list of roles where a fake role is going to be found (if exists)
        :param uow: unit of work
        :return: fake role's uuid or None if it does not exist
        """
        for role_uuid in roles:
            role = await self.get_role(uow, role_uuid)
            if not role:
                return role_uuid

    async def has_permission(self, uow: IUnitOfWork, user: UserRead | UserCreate | UserUpdate, permission: str):
        for role_uuid in user.roles:
            role = await self.get_role(uow, role_uuid)
            if role and permission in role.permissions:
                return True
        return False
