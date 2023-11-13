from uuid import UUID

from fastapi import APIRouter
from fastapi_cache.decorator import cache
from fastapi_cache import FastAPICache

from utils.exceptions import DifferentUuidsError, try_except_decorator
from utils.logic import same_uuids
from utils.dependency import (AuthenticationServiceDep,
                              InventoryServiceDep,
                              RolesServiceDep,
                              UsersServiceDep,
                              AuthenticationDep,
                              UOWDep)

from users.exceptions import UserNotFoundError
from authentication.exceptions import NotAuthenticatedError
from records.logic import validate_price

from .schemas import InventoryItemCreate, InventoryItemUpdate
from .exceptions import *

router = APIRouter(prefix='/inventory', tags=['Inventory'])


@router.get('')
@cache(namespace='inventory', expire=3600)
@try_except_decorator
async def get_inventory_items_handler(uow: UOWDep,
                                      authentication_service: AuthenticationServiceDep,
                                      inventory_service: InventoryServiceDep,
                                      roles_service: RolesServiceDep,
                                      users_service: UsersServiceDep,
                                      user_uuid: UUID | None = None,
                                      authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    if not user_uuid or not same_uuids(author.uuid, user_uuid):
        can_read = await roles_service.has_permission(uow, author, 'read_inventory')
        if not can_read:
            raise ReadInventoryDenied

    if user_uuid and same_uuids(author.uuid, user_uuid):
        inventory_items = await inventory_service.get_inventory_items(uow, user_uuid=author.uuid)
    elif user_uuid:
        user = users_service.get_user(user_uuid)
        if not user:
            raise UserNotFoundError
        inventory_items = await inventory_service.get_inventory_items(uow, user_uuid=user.uuid)
    else:
        inventory_items = await inventory_service.get_inventory_items(uow)

    return {
        'data': inventory_items,
        'details': 'Inventory items were selected.'
    }


@router.get('/{uuid}')
@cache(namespace='inventory', expire=3600)
@try_except_decorator
async def get_inventory_item_handler(uow: UOWDep,
                                     authentication_service: AuthenticationServiceDep,
                                     inventory_service: InventoryServiceDep,
                                     roles_service: RolesServiceDep,
                                     uuid: UUID,
                                     authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    inventory_item = await inventory_service.get_inventory_item(uow, uuid)
    if not inventory_item:
        raise InventoryItemNotFoundError

    if not same_uuids(author.uuid, inventory_item.user_uuid):
        can_read = await roles_service.has_permission(uow, author, 'read_inventory')
        if not can_read:
            raise ReadInventoryDenied

    return {
        'data': inventory_item,
        'details': 'Inventory item was selected.'
    }


@router.post('/{uuid}')
@try_except_decorator
async def post_inventory_item_handler(uow: UOWDep,
                                      authentication_service: AuthenticationServiceDep,
                                      inventory_service: InventoryServiceDep,
                                      roles_service: RolesServiceDep,
                                      users_service: UsersServiceDep,
                                      uuid: UUID,
                                      inventory_item: InventoryItemCreate,
                                      authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    if not same_uuids(inventory_item.uuid, uuid):
        raise DifferentUuidsError

    if not same_uuids(author.uuid, inventory_item.user_uuid):
        can_insert = await roles_service.has_permission(uow, author, 'insert_inventory')
        if not can_insert:
            raise InsertInventoryDenied

        user = users_service.get_user(uow, inventory_item.user_uuid)
        if not user:
            raise UserNotFoundError

    item_with_same_uuid = await inventory_service.get_inventory_item(uow, uuid)
    if item_with_same_uuid:
        raise InventoryItemExistsError

    await inventory_service.add_inventory_item(uow, inventory_item)
    await FastAPICache.clear(namespace='inventory')
    return {
        'data': None,
        'details': 'Inventory item was added.'
    }


@router.put('/{uuid}')
@try_except_decorator
async def put_inventory_item_handler(uow: UOWDep,
                                     authentication_service: AuthenticationServiceDep,
                                     inventory_service: InventoryServiceDep,
                                     roles_service: RolesServiceDep,
                                     users_service: RolesServiceDep,
                                     uuid: UUID,
                                     inventory_item: InventoryItemUpdate,
                                     authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    if not same_uuids(inventory_item.uuid, uuid):
        raise DifferentUuidsError

    if not same_uuids(author.uuid, inventory_item.user_uuid):
        can_update = await roles_service.has_permission(uow, author, 'update_inventory')
        if not can_update:
            raise UpdateInventoryDenied

        user = users_service.get_user(uow, inventory_item.user_uuid)
        if not user:
            raise UserNotFoundError

    item_with_this_uuid = await inventory_service.get_inventory_item(uow, uuid)
    if not item_with_this_uuid:
        raise InventoryItemNotFoundError

    validate_price(inventory_item.price)

    await inventory_service.update_inventory_item(uow, inventory_item)
    await FastAPICache.clear(namespace='inventory')
    return {
        'data': None,
        'details': 'Inventory item was updated.'
    }


@router.delete('/{uuid}')
@try_except_decorator
async def delete_inventory_item_handler(uow: UOWDep,
                                        authentication_service: AuthenticationServiceDep,
                                        inventory_service: InventoryServiceDep,
                                        roles_service: RolesServiceDep,
                                        uuid: UUID,
                                        authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    item_with_this_uuid = await inventory_service.get_inventory_item(uow, uuid)
    if not item_with_this_uuid:
        raise InventoryItemNotFoundError

    if not same_uuids(author.uuid, item_with_this_uuid.user_uuid):
        can_delete = await roles_service.has_permission(uow, author, 'delete_inventory')
        if not can_delete:
            raise DeleteInventoryDenied

    await inventory_service.delete_inventory_item(uow, uuid)
    await FastAPICache.clear(namespace='inventory')
    return {
        'data': None,
        'details': 'Inventory item was deleted.'
    }
