from uuid import UUID, uuid4

from fastapi import APIRouter, BackgroundTasks

from utils.logic import same_uuids
from utils.exceptions import DifferentUuidsError, try_except_decorator
from utils.dependency import (RecordsServiceDep,
                              AuthenticationServiceDep,
                              RolesServiceDep,
                              SkinsServiceDep,
                              AuthenticationDep,
                              InsertAccessKeyDep,
                              UOWDep,
                              FileDep,
                              DatetimeFormDep)

from authentication.exceptions import NotAuthenticatedError
from skins.exceptions import SkinNotFoundError

from .schemas import RecordCreate, RecordUpdate
from .logic import *
from .exceptions import *

router = APIRouter(prefix='/records', tags=['Records'])


@router.get('')
@try_except_decorator
async def get_records_handler(records_service: RecordsServiceDep,
                              authentication_service: AuthenticationServiceDep,
                              roles_service: RolesServiceDep,
                              uow: UOWDep,
                              skin_uuid: UUID,
                              year: int,
                              month: int,
                              day: int | None = None,
                              hour: int | None = None,
                              authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    can_read = await roles_service.has_permission(uow, author, 'read_records')
    if not can_read:
        raise ReadRecordDenied

    validate_year(year)
    validate_month(month)
    if day:
        validate_day(year, month, day)
        if hour:
            validate_hour(hour)

    records = await records_service.get_records(uow, skin_uuid=skin_uuid, year=year,
                                                month=month, day=day, hour=hour)
    return {
        'data': records,
        'details': 'Records were selected.'
    }


@router.get('/{uuid}')
@try_except_decorator
async def get_record_handler(records_service: RecordsServiceDep,
                             authentication_service: AuthenticationServiceDep,
                             roles_service: RolesServiceDep,
                             uow: UOWDep,
                             uuid: UUID,
                             authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    can_read = await roles_service.has_permission(uow, author, 'read_records')
    if not can_read:
        raise ReadRecordDenied

    record = await records_service.get_record(uow, uuid)
    if not record:
        raise RecordNotFoundError

    return {
        'data': record,
        'details': 'Record was selected.'
    }


async def add_records_image(registered_at: datetime, screenshot: bytes, skins_service, records_service, uow):
    code, result = parse_screenshot(screenshot)
    print(code, result)
    if code == 0:
        for skin_record in result:
            try:
                skins_with_this_name = await skins_service.get_skins(uow, name=skin_record['name'])
                if not skins_with_this_name:
                    continue
                skin_uuid = skins_with_this_name[0].uuid

                record_with_this_skin_and_this_time = await records_service.get_records(uow, skin_uuid=skin_uuid,
                                                                                        registered_at=registered_at.replace(tzinfo=None))
                if record_with_this_skin_and_this_time:
                    continue

                record = RecordCreate(uuid=uuid4(),
                                      registered_at=registered_at,
                                      skin_uuid=skin_uuid,
                                      price=skin_record['price'],
                                      count=skin_record['count'])
                await records_service.add_record(uow, record)
            except Exception as ex:
                print(ex)


@router.post('/image')
@try_except_decorator
async def post_records_image_handler(records_service: RecordsServiceDep,
                                     authentication_service: AuthenticationServiceDep,
                                     roles_service: RolesServiceDep,
                                     skins_service: SkinsServiceDep,
                                     background_tasks: BackgroundTasks,
                                     uow: UOWDep,
                                     screenshot: FileDep,
                                     registered_at: DatetimeFormDep,
                                     insert_access_key: InsertAccessKeyDep = None,
                                     authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)

    can_insert = False
    if author:
        can_insert = await roles_service.has_permission(uow, author, 'insert_records')
    if not can_insert:
        can_insert = records_service.has_insert_access(insert_access_key)
    if not can_insert:
        raise InsertRecordDenied

    background_tasks.add_task(add_records_image, registered_at, screenshot, skins_service, records_service, uow)

    return {
        'data': None,
        'details': 'Image was accepted. After it is processed, records will be added (if possible).'
    }


@router.post('/{uuid}')
@try_except_decorator
async def post_records_handler(record: RecordCreate,
                               records_service: RecordsServiceDep,
                               authentication_service: AuthenticationServiceDep,
                               roles_service: RolesServiceDep,
                               skins_service: SkinsServiceDep,
                               uow: UOWDep,
                               uuid: UUID,
                               insert_access_key: InsertAccessKeyDep = None,
                               authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)

    validate_price(record.price)

    if not same_uuids(record.uuid, uuid):
        raise DifferentUuidsError

    record_with_same_uuid = await records_service.get_record(uow, uuid)
    if record_with_same_uuid:
        raise RecordExistsError

    can_insert = False
    if author:
        can_insert = await roles_service.has_permission(uow, author, 'insert_records')
    if not can_insert:
        can_insert = records_service.has_insert_access(insert_access_key)
    if not can_insert:
        raise InsertRecordDenied

    skin_with_this_uuid = await skins_service.get_skin(uow, record.skin_uuid)
    if not skin_with_this_uuid:
        raise SkinNotFoundError

    await records_service.add_record(uow, record)
    return {
        'data': None,
        'details': 'Record was added.'
    }


@router.put('/{uuid}')
@try_except_decorator
async def put_records_handler(record: RecordUpdate,
                              records_service: RecordsServiceDep,
                              authentication_service: AuthenticationServiceDep,
                              roles_service: RolesServiceDep,
                              skins_service: SkinsServiceDep,
                              uow: UOWDep,
                              uuid: UUID,
                              authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    validate_price(record.price)

    if not same_uuids(record.uuid, uuid):
        raise DifferentUuidsError

    record_with_this_uuid = await records_service.get_record(uow, uuid)
    if not record_with_this_uuid:
        raise RecordNotFoundError

    can_update = await roles_service.has_permission(uow, author, 'update_records')
    if not can_update:
        raise UpdateRecordDenied

    skin_with_this_uuid = await skins_service.get_skin(uow, record.skin_uuid)
    if not skin_with_this_uuid:
        raise SkinNotFoundError

    await records_service.update_record(uow, record)
    return {
        'data': None,
        'details': 'Record was updated.'
    }


@router.delete('/{uuid}')
@try_except_decorator
async def delete_record_handler(records_service: RecordsServiceDep,
                                authentication_service: AuthenticationServiceDep,
                                roles_service: RolesServiceDep,
                                uow: UOWDep,
                                uuid: UUID,
                                authorization: AuthenticationDep = None):
    author = await authentication_service.is_signed_in(uow, authorization)
    if not author:
        raise NotAuthenticatedError

    can_delete = await roles_service.has_permission(uow, author, 'delete_records')
    if not can_delete:
        raise DeleteRecordDenied

    record = await records_service.get_record(uow, uuid)
    if not record:
        raise RecordNotFoundError

    await records_service.delete_record(uow, uuid)
    return {
        'data': None,
        'details': 'Record was deleted.'
    }
