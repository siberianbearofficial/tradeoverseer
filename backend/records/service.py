from uuid import UUID
from datetime import datetime

from utils.unitofwork import IUnitOfWork
from utils.config import INSERT_ACCESS_KEY

from .repository import RecordsRepository
from .schemas import RecordCreate, RecordUpdate
from .logic import get_period_boundaries


class RecordsService:
    def __init__(self, records_repository: RecordsRepository):
        self.records_repository = records_repository

    async def get_records(self, uow: IUnitOfWork, skin_uuid: UUID, year: int | None = None, month: int | None = None,
                          day: int | None = None, hour: int | None = None, registered_at: datetime | None = None):
        async with uow:
            if registered_at:
                records = await self.records_repository.find_all(uow.session, skin_uuid=skin_uuid,
                                                                 registered_at=registered_at)
            else:
                period_boundaries = get_period_boundaries(year, month, day, hour)
                records = await self.records_repository.find_all(uow.session, {
                    'registered_at': ('between', *period_boundaries)
                }, skin_uuid=skin_uuid)
            return records

    async def get_record(self, uow: IUnitOfWork, uuid: UUID):
        async with uow:
            record = await self.records_repository.find_one(uow.session, uuid=uuid)
            return record

    async def add_record(self, uow: IUnitOfWork, record: RecordCreate):
        async with uow:
            latest_with_this_skin = await self.records_repository.find_latest(uow.session, skin_uuid=record.skin_uuid)
            if latest_with_this_skin:
                latest_price = float(latest_with_this_skin.price)
                current_price = float(record.price)

                if int(abs(latest_price - current_price) / max(latest_price, current_price) * 100) > 50:
                    raise ValueError('Invalid price. The previous value differs by more than 50%.')

            record_dict = {
                'uuid': record.uuid,
                'registered_at': record.registered_at.replace(tzinfo=None),
                'skin_uuid': record.skin_uuid,
                'price': record.price,
                'count': record.count
            }
            await self.records_repository.add_one(uow.session, record_dict)
            await uow.commit()

    async def update_record(self, uow: IUnitOfWork, record: RecordUpdate):
        async with uow:
            record_dict = {
                'uuid': record.uuid,
                'registered_at': record.registered_at.replace(tzinfo=None),
                'skin_uuid': record.skin_uuid,
                'price': record.price,
                'count': record.count
            }
            await self.records_repository.edit_one(uow.session, record.uuid, record_dict)
            await uow.commit()

    async def delete_record(self, uow: IUnitOfWork, uuid: UUID):
        async with uow:
            await self.records_repository.delete_one(uow.session, uuid)
            await uow.commit()

    @staticmethod
    def has_insert_access(insert_access: str | None = None):
        if insert_access:
            if insert_access.strip() == INSERT_ACCESS_KEY:
                return True
        return False
