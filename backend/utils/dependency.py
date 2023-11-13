from typing import Annotated
from datetime import datetime

from fastapi import Depends, Header, File, Form

from authentication.service import AuthenticationService

from roles.repository import RolesRepository
from roles.service import RolesService

from users.repository import UsersRepository
from users.service import UsersService

from records.repository import RecordsRepository
from records.service import RecordsService

from skins.repository import SkinsRepository
from skins.service import SkinsService

from inventory.repository import InventoryRepository
from inventory.service import InventoryService

from rarities.repository import RaritiesRepository
from rarities.service import RaritiesService

from orders.service import OrdersService

from .unitofwork import IUnitOfWork, UnitOfWork

roles_repository = RolesRepository()
roles_service = RolesService(roles_repository)

inventory_repository = InventoryRepository()
inventory_service = InventoryService(inventory_repository)

users_repository = UsersRepository()
users_service = UsersService(users_repository)

authentication_service = AuthenticationService(users_service)

records_repository = RecordsRepository()
records_service = RecordsService(records_repository)

skins_repository = SkinsRepository()
skins_service = SkinsService(skins_repository)

rarities_repository = RaritiesRepository()
rarities_service = RaritiesService(rarities_repository)

orders_service = OrdersService()


async def get_users_service():
    return users_service


async def get_authentication_service():
    return authentication_service


async def get_records_service():
    return records_service


async def get_skins_service():
    return skins_service


async def get_inventory_service():
    return inventory_service


async def get_roles_service():
    return roles_service


async def get_rarities_service():
    return rarities_service


async def get_orders_service():
    return orders_service


UsersServiceDep = Annotated[UsersService, Depends(get_users_service)]
AuthenticationServiceDep = Annotated[AuthenticationService, Depends(get_authentication_service)]
RecordsServiceDep = Annotated[RecordsService, Depends(get_records_service)]
SkinsServiceDep = Annotated[SkinsService, Depends(get_skins_service)]
InventoryServiceDep = Annotated[InventoryService, Depends(get_inventory_service)]
RolesServiceDep = Annotated[RolesService, Depends(get_roles_service)]
RaritiesServiceDep = Annotated[RaritiesService, Depends(get_rarities_service)]
OrdersServiceDep = Annotated[OrdersService, Depends(get_orders_service)]

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
AuthenticationDep = Annotated[str | None, Header()]
InsertAccessKeyDep = Annotated[str | None, Header()]
FileDep = Annotated[bytes, File()]
DatetimeFormDep = Annotated[datetime, Form()]
