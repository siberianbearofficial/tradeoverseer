from uuid import UUID

from fastapi import APIRouter
from fastapi_cache.decorator import cache
from fastapi_cache import FastAPICache

from utils.logic import same_uuids, check_password
from utils.exceptions import DifferentUuidsError, try_except_decorator
from utils.dependency import (UsersServiceDep,
                              AuthenticationServiceDep,
                              InventoryServiceDep,
                              RolesServiceDep,
                              AuthenticationDep,
                              UOWDep)

from authentication.exceptions import NotAuthenticatedError, IncorrectCredentialsError
from roles.exceptions import RoleNotFoundError

from .schemas import UserCreate, UserUpdate, ChangePassword
from .exceptions import *
from .logic import validate_username, validate_password

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('')
@cache(namespace='users', expire=3600)
@try_except_decorator
async def get_users_handler(users_service: UsersServiceDep,
                            uow: UOWDep,
                            username: str | None = None):
    users = await users_service.get_users(uow, username=username)
    return {
        'data': users,
        'details': 'Users were selected.'
    }


@router.get('/{uuid}')
@cache(namespace='users', expire=3600)
@try_except_decorator
async def get_user_handler(users_service: UsersServiceDep,
                           uow: UOWDep,
                           uuid: UUID):
    user = await users_service.get_user(uow, uuid)
    if not user:
        raise UserNotFoundError

    return {
        'data': user,
        'details': 'User was selected.'
    }


@router.post('/{uuid}')
@try_except_decorator
async def post_users_handler(users_service: UsersServiceDep,
                             authentication_service: AuthenticationServiceDep,
                             roles_service: RolesServiceDep,
                             uow: UOWDep,
                             uuid: UUID,
                             user: UserCreate,
                             authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    if not same_uuids(user.uuid, uuid):
        raise DifferentUuidsError

    validate_username(user.username)
    validate_password(user.password)

    user_with_this_uuid = await users_service.get_user(uow, user.uuid)
    if user_with_this_uuid:
        raise UserExistsError

    users_with_same_usernames = await users_service.get_users(uow, username=user.username)
    if users_with_same_usernames:
        raise UsernameTakenError

    can_insert = await roles_service.has_permission(uow, author, 'insert_users')
    if not can_insert:
        raise InsertUserDenied

    fake_role = await roles_service.get_fake_role(uow, user.roles)
    if fake_role:
        raise RoleNotFoundError

    await users_service.add_user(uow, user)
    await FastAPICache.clear(namespace='users')
    await FastAPICache.clear(namespace='inventory')
    return {
        'data': None,
        'details': 'User was added.'
    }


@router.put('/{uuid}')
@try_except_decorator
async def put_users_handler(users_service: UsersServiceDep,
                            authentication_service: AuthenticationServiceDep,
                            roles_service: RolesServiceDep,
                            uow: UOWDep,
                            uuid: UUID,
                            user: UserUpdate,
                            authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    if not same_uuids(user.uuid, uuid):
        raise DifferentUuidsError

    validate_username(user.username)

    can_update = False
    if not same_uuids(author.uuid, user.uuid):
        can_update = await roles_service.has_permission(uow, author, 'update_users')
        if not can_update:
            raise UpdateUserDenied

        user_with_this_uuid = await users_service.get_user(uow, user.uuid)
        if not user_with_this_uuid:
            raise UserNotFoundError

    users_with_new_username = await users_service.get_users(uow, username=user.username)
    if users_with_new_username and not same_uuids(users_with_new_username[0].uuid, user.uuid):
        raise UsernameTakenError

    if can_update:
        fake_role = await roles_service.get_fake_role(uow, user.roles)
        if fake_role:
            raise RoleNotFoundError

        await users_service.update_user(uow, user, full_update=True)
    else:
        await users_service.update_user(uow, user)
    await FastAPICache.clear(namespace='users')
    await FastAPICache.clear(namespace='inventory')
    return {
        'data': None,
        'details': 'User was updated.'
    }


@router.put('/{uuid}/password')
@try_except_decorator
async def put_users_password_handler(users_service: UsersServiceDep,
                                     authentication_service: AuthenticationServiceDep,
                                     uow: UOWDep,
                                     uuid: UUID,
                                     change_password: ChangePassword,
                                     authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    if not same_uuids(author.uuid, uuid):
        raise ChangePasswordDenied

    validate_password(change_password.new_password)

    user_with_this_uuid = await users_service.get_user(uow, uuid, with_password=True)
    if not user_with_this_uuid:
        raise UserNotFoundError

    if not check_password(change_password.current_password, user_with_this_uuid.hashed_password):
        raise IncorrectCredentialsError

    await users_service.change_password(uow, uuid, change_password)
    await FastAPICache.clear(namespace='users')
    await FastAPICache.clear(namespace='inventory')
    return {
        'data': None,
        'details': 'Password was changed.'
    }


@router.delete('/{uuid}')
@try_except_decorator
async def delete_user_handler(users_service: UsersServiceDep,
                              authentication_service: AuthenticationServiceDep,
                              roles_service: RolesServiceDep,
                              inventory_service: InventoryServiceDep,
                              uow: UOWDep,
                              uuid: UUID,
                              authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    user_with_this_uuid = await users_service.get_user(uow, uuid)
    if not user_with_this_uuid:
        raise UserNotFoundError

    if not same_uuids(author.uuid, user_with_this_uuid.uuid):
        can_delete = await roles_service.has_permission(uow, author, 'delete_users')
        if not can_delete:
            raise DeleteUserDenied

    await inventory_service.delete_inventory_items(uow, user_with_this_uuid.uuid)
    await users_service.delete_user(uow, user_with_this_uuid.uuid)
    await FastAPICache.clear(namespace='users')
    await FastAPICache.clear(namespace='inventory')
    return {
        'data': None,
        'details': 'User was deleted.'
    }
