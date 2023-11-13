from uuid import UUID

from fastapi import APIRouter
from fastapi_cache.decorator import cache
from fastapi_cache import FastAPICache

from utils.logic import same_uuids
from utils.exceptions import DifferentUuidsError, try_except_decorator
from utils.dependency import (SkinsServiceDep,
                              AuthenticationDep,
                              RolesServiceDep,
                              UOWDep,
                              AuthenticationServiceDep)

from authentication.exceptions import NotAuthenticatedError

from .exceptions import *
from .schemas import SkinCreate, SkinUpdate

router = APIRouter(prefix='/skins', tags=['Skins'])


@router.get('')
@cache(namespace='skins', expire=3600)
@try_except_decorator
async def get_skins_handler(skins_service: SkinsServiceDep,
                            authentication_service: AuthenticationServiceDep,
                            roles_service: RolesServiceDep,
                            uow: UOWDep,
                            name: str | None = None,
                            authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    can_read = await roles_service.has_permission(uow, author, 'read_skins')
    if not can_read:
        raise ReadSkinDenied

    skins = await skins_service.get_skins(uow, name=name)
    return {
        'data': skins,
        'details': 'Skins were selected.'
    }


@router.get('/{uuid}')
@cache(namespace='skins', expire=3600)
@try_except_decorator
async def get_skin_handler(skins_service: SkinsServiceDep,
                           authentication_service: AuthenticationServiceDep,
                           roles_service: RolesServiceDep,
                           uow: UOWDep,
                           uuid: UUID,
                           authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    can_read = await roles_service.has_permission(uow, author, 'read_skins')
    if not can_read:
        raise ReadSkinDenied

    skin = await skins_service.get_skin(uow, uuid)
    if not skin:
        raise SkinNotFoundError

    return {
        'data': skin,
        'details': 'Skin was selected.'
    }


@router.post('/{uuid}')
@try_except_decorator
async def post_skin_handler(uow: UOWDep,
                            authentication_service: AuthenticationServiceDep,
                            roles_service: RolesServiceDep,
                            skins_service: SkinsServiceDep,
                            uuid: UUID,
                            skin: SkinCreate,
                            authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    if not same_uuids(skin.uuid, uuid):
        raise DifferentUuidsError

    skin_with_same_uuid = await skins_service.get_skin(uow, uuid)
    if skin_with_same_uuid:
        raise SkinExistsError

    can_insert = await roles_service.has_permission(uow, author, 'insert_skins')
    if not can_insert:
        raise InsertSkinDenied

    await skins_service.add_skin(uow, skin)
    await FastAPICache.clear(namespace='skins')
    await FastAPICache.clear(namespace='inventory')
    return {
        'data': None,
        'details': 'Skin was added.'
    }


@router.put('/{uuid}')
@try_except_decorator
async def put_skin_handler(uow: UOWDep,
                           authentication_service: AuthenticationServiceDep,
                           roles_service: RolesServiceDep,
                           skins_service: SkinsServiceDep,
                           uuid: UUID,
                           skin: SkinUpdate,
                           authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    if not same_uuids(skin.uuid, uuid):
        raise DifferentUuidsError

    skin_with_this_uuid = await skins_service.get_skin(uow, uuid)
    if not skin_with_this_uuid:
        raise SkinNotFoundError

    can_update = await roles_service.has_permission(uow, author, 'update_skins')
    if not can_update:
        raise UpdateSkinDenied

    await skins_service.update_skin(uow, skin)
    await FastAPICache.clear(namespace='skins')
    await FastAPICache.clear(namespace='inventory')
    return {
        'data': None,
        'details': 'Skin was updated.'
    }


@router.delete('/{uuid}')
@try_except_decorator
async def delete_skin_handler(uow: UOWDep,
                              authentication_service: AuthenticationServiceDep,
                              roles_service: RolesServiceDep,
                              skins_service: SkinsServiceDep,
                              uuid: UUID,
                              authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    skin_with_this_uuid = await skins_service.get_skin(uow, uuid)
    if not skin_with_this_uuid:
        raise SkinNotFoundError

    can_delete = await roles_service.has_permission(uow, author, 'delete_skins')
    if not can_delete:
        raise DeleteSkinDenied

    await skins_service.delete_skin(uow, uuid)
    await FastAPICache.clear(namespace='skins')
    await FastAPICache.clear(namespace='inventory')
    return {
        'data': None,
        'details': 'Skin was deleted.'
    }
