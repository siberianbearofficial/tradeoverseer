from fastapi import APIRouter

from utils.logic import check_password
from utils.exceptions import try_except_decorator
from utils.dependency import UsersServiceDep, UOWDep

from users.exceptions import UserNotFoundError

from .schemas import SignIn
from .exceptions import IncorrectCredentialsError
from .logic import *

router = APIRouter(prefix='/sign-in', tags=['Authentication'])


@router.post('')
@try_except_decorator
async def post_sign_in_handler(users_service: UsersServiceDep,
                               uow: UOWDep,
                               sign_in: SignIn):
    users = await users_service.get_users(uow, username=sign_in.username, with_password=True)
    if not users:
        raise UserNotFoundError

    if not check_password(sign_in.password, users[0].hashed_password):
        raise IncorrectCredentialsError

    payload = await get_payload(users[0].uuid, users[0].roles)
    return payload
