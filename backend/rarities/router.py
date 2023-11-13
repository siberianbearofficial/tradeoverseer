from uuid import UUID

from fastapi import APIRouter
from fastapi_cache.decorator import cache
from fastapi_cache import FastAPICache

from utils.logic import same_uuids
from utils.exceptions import DifferentUuidsError, try_except_decorator
from utils.dependency import (RaritiesServiceDep,
                              AuthenticationDep,
                              RolesServiceDep,
                              UOWDep,
                              AuthenticationServiceDep)

from authentication.exceptions import NotAuthenticatedError

from .exceptions import *
from .schemas import RarityCreate, RarityUpdate

router = APIRouter(prefix='/rarities', tags=['Rarities'])


@router.get('')
@cache(namespace='rarities', expire=3600)
@try_except_decorator
async def get_rarities_handler(rarities_service: RaritiesServiceDep,
                               authentication_service: AuthenticationServiceDep,
                               roles_service: RolesServiceDep,
                               uow: UOWDep,
                               name: str | None = None,
                               authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    can_read = await roles_service.has_permission(uow, author, 'read_rarities')
    if not can_read:
        raise ReadRarityDenied

    rarities = await rarities_service.get_rarities(uow, name=name)
    return {
        'data': rarities,
        'details': 'Rarities were selected.'
    }


@router.get('/{uuid}')
@cache(namespace='rarities', expire=3600)
@try_except_decorator
async def get_rarity_handler(rarities_service: RaritiesServiceDep,
                             authentication_service: AuthenticationServiceDep,
                             roles_service: RolesServiceDep,
                             uow: UOWDep,
                             uuid: UUID,
                             authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    can_read = await roles_service.has_permission(uow, author, 'read_rarities')
    if not can_read:
        raise ReadRarityDenied

    rarity = await rarities_service.get_rarity(uow, uuid)
    if not rarity:
        raise RarityNotFoundError

    return {
        'data': rarity,
        'details': 'Rarity was selected.'
    }


@router.post('/{uuid}')
@try_except_decorator
async def post_rarity_handler(uow: UOWDep,
                              authentication_service: AuthenticationServiceDep,
                              roles_service: RolesServiceDep,
                              rarities_service: RaritiesServiceDep,
                              uuid: UUID,
                              rarity: RarityCreate,
                              authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    if not same_uuids(rarity.uuid, uuid):
        raise DifferentUuidsError

    rarity_with_same_uuid = await rarities_service.get_rarity(uow, uuid)
    if rarity_with_same_uuid:
        raise RarityExistsError

    can_insert = await roles_service.has_permission(uow, author, 'insert_rarities')
    if not can_insert:
        raise InsertRarityDenied

    await rarities_service.add_rarity(uow, rarity)
    await FastAPICache.clear(namespace='rarities')
    await FastAPICache.clear(namespace='skins')
    return {
        'data': None,
        'details': 'Rarity was added.'
    }


@router.put('/{uuid}')
@try_except_decorator
async def put_rarity_handler(uow: UOWDep,
                             authentication_service: AuthenticationServiceDep,
                             roles_service: RolesServiceDep,
                             rarities_service: RaritiesServiceDep,
                             uuid: UUID,
                             rarity: RarityUpdate,
                             authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    if not same_uuids(rarity.uuid, uuid):
        raise DifferentUuidsError

    rarity_with_this_uuid = await rarities_service.get_rarity(uow, uuid)
    if not rarity_with_this_uuid:
        raise RarityNotFoundError

    can_update = await roles_service.has_permission(uow, author, 'update_rarities')
    if not can_update:
        raise UpdateRarityDenied

    await rarities_service.update_rarity(uow, rarity)
    await FastAPICache.clear(namespace='rarities')
    await FastAPICache.clear(namespace='skins')
    return {
        'data': None,
        'details': 'Rarity was updated.'
    }


@router.delete('/{uuid}')
@try_except_decorator
async def delete_rarity_handler(uow: UOWDep,
                                authentication_service: AuthenticationServiceDep,
                                roles_service: RolesServiceDep,
                                rarities_service: RaritiesServiceDep,
                                uuid: UUID,
                                authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    rarity_with_this_uuid = await rarities_service.get_rarity(uow, uuid)
    if not rarity_with_this_uuid:
        raise RarityNotFoundError

    can_delete = await roles_service.has_permission(uow, author, 'delete_rarities')
    if not can_delete:
        raise DeleteRarityDenied

    await rarities_service.delete_rarity(uow, uuid)
    await FastAPICache.clear(namespace='rarities')
    await FastAPICache.clear(namespace='skins')
    return {
        'data': None,
        'details': 'Rarity was deleted.'
    }
