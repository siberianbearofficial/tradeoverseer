from uuid import UUID

from fastapi import APIRouter
from fastapi_cache.decorator import cache
from fastapi_cache import FastAPICache

from utils.logic import same_uuids
from utils.exceptions import DifferentUuidsError, try_except_decorator
from utils.dependency import (AuthenticationServiceDep,
                              RolesServiceDep,
                              AuthenticationDep,
                              UOWDep)

from authentication.exceptions import NotAuthenticatedError

from .schemas import RoleCreate, RoleUpdate
from .exceptions import *

router = APIRouter(prefix='/roles', tags=['Roles'])


@router.get('')
@cache(namespace='roles', expire=3600)
@try_except_decorator
async def get_roles_handler(roles_service: RolesServiceDep,
                            authentication_service: AuthenticationServiceDep,
                            uow: UOWDep,
                            name: str | None = None,
                            authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    can_read = await roles_service.has_permission(uow, author, 'read_roles')
    if not can_read:
        raise ReadRoleDenied

    roles = await roles_service.get_roles(uow, name=name)
    return {
        'data': roles,
        'details': 'Roles were selected.'
    }


@router.get('/{uuid}')
@cache(namespace='roles', expire=3600)
@try_except_decorator
async def get_role_handler(authentication_service: AuthenticationServiceDep,
                           roles_service: RolesServiceDep,
                           uow: UOWDep,
                           uuid: UUID,
                           authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    can_read = await roles_service.has_permission(uow, author, 'read_roles')
    if not can_read:
        raise ReadRoleDenied

    role = await roles_service.get_role(uow, uuid)
    if not role:
        raise RoleNotFoundError

    return {
        'data': role,
        'details': 'Role was selected.'
    }


@router.post('/{uuid}')
@try_except_decorator
async def post_role_handler(uow: UOWDep,
                            authentication_service: AuthenticationServiceDep,
                            roles_service: RolesServiceDep,
                            uuid: UUID,
                            role: RoleCreate,
                            authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    if not same_uuids(role.uuid, uuid):
        raise DifferentUuidsError

    role_with_same_uuid = await roles_service.get_role(uow, uuid)
    if role_with_same_uuid:
        raise RoleExistsError

    can_insert = await roles_service.has_permission(uow, author, 'insert_roles')
    if not can_insert:
        raise InsertRoleDenied

    await roles_service.add_role(uow, role)
    await FastAPICache.clear(namespace='roles')
    await FastAPICache.clear(namespace='users')
    return {
        'data': None,
        'details': 'Role was added.'
    }


@router.put('/{uuid}')
@try_except_decorator
async def put_role_handler(uow: UOWDep,
                           authentication_service: AuthenticationServiceDep,
                           roles_service: RolesServiceDep,
                           uuid: UUID,
                           role: RoleUpdate,
                           authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    if not same_uuids(role.uuid, uuid):
        raise DifferentUuidsError

    role_with_this_uuid = await roles_service.get_role(uow, uuid)
    if not role_with_this_uuid:
        raise RoleNotFoundError

    can_update = await roles_service.has_permission(uow, author, 'update_roles')
    if not can_update:
        raise UpdateRoleDenied

    await roles_service.update_role(uow, role)
    await FastAPICache.clear(namespace='roles')
    await FastAPICache.clear(namespace='users')
    return {
        'data': None,
        'details': 'Role was updated.'
    }


@router.delete('/{uuid}')
@try_except_decorator
async def delete_role_handler(uow: UOWDep,
                              authentication_service: AuthenticationServiceDep,
                              roles_service: RolesServiceDep,
                              uuid: UUID,
                              authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    role_with_this_uuid = await roles_service.get_role(uow, uuid)
    if not role_with_this_uuid:
        raise RoleNotFoundError

    can_delete = await roles_service.has_permission(uow, author, 'delete_roles')
    if not can_delete:
        raise DeleteRoleDenied

    await roles_service.delete_role(uow, uuid)
    await FastAPICache.clear(namespace='roles')
    await FastAPICache.clear(namespace='users')
    return {
        'data': None,
        'details': 'Role was deleted.'
    }
