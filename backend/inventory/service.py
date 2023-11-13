from uuid import UUID

from utils.unitofwork import IUnitOfWork

from .repository import InventoryRepository
from .schemas import InventoryItemCreate, InventoryItemUpdate


class InventoryService:
    def __init__(self, inventory_repository: InventoryRepository):
        self.inventory_repository = inventory_repository

    async def get_inventory_items(self, uow: IUnitOfWork, user_uuid: UUID | None = None):
        filter_by_dict = {'user_uuid': user_uuid} if user_uuid else {}
        async with uow:
            inventory_items = await self.inventory_repository.find_all(uow.session, **filter_by_dict)
            return inventory_items

    async def get_inventory_item(self, uow: IUnitOfWork, uuid: UUID):
        async with uow:
            inventory_item = await self.inventory_repository.find_one(uow.session, uuid=uuid)
            return inventory_item

    async def add_inventory_item(self, uow: IUnitOfWork, item: InventoryItemCreate):
        async with uow:
            item_dict = {
                'uuid': item.uuid,
                'user_uuid': item.user_uuid,
                'skin_uuid': item.skin_uuid,
                'added_at': item.added_at.replace(tzinfo=None),
                'price': item.price,
                'count': item.count
            }
            await self.inventory_repository.add_one(uow.session, item_dict)
            await uow.commit()

    async def update_inventory_item(self, uow: IUnitOfWork, item: InventoryItemUpdate):
        async with uow:
            item_dict = {
                'skin_uuid': item.skin_uuid,
                'added_at': item.added_at.replace(tzinfo=None),
                'price': item.price,
                'count': item.count
            }
            await self.inventory_repository.edit_one(uow.session, item.uuid, item_dict)
            await uow.commit()

    async def delete_inventory_item(self, uow: IUnitOfWork, uuid: UUID):
        async with uow:
            await self.inventory_repository.delete_one(uow.session, uuid)
            await uow.commit()

    async def delete_inventory_items(self, uow: IUnitOfWork, user_uuid: UUID | None = None):
        filter_by_dict = {'user_uuid': user_uuid} if user_uuid else {}
        async with uow:
            await self.inventory_repository.delete_all(uow.session, **filter_by_dict)
            await uow.commit()
