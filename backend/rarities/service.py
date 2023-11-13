from uuid import UUID

from utils.unitofwork import IUnitOfWork

from .repository import RaritiesRepository
from .schemas import RarityCreate, RarityUpdate


class RaritiesService:
    def __init__(self, rarities_repository: RaritiesRepository):
        self.rarities_repository = rarities_repository

    async def get_rarities(self, uow: IUnitOfWork, name: str | None = None):
        filter_by_dict = {'name': name} if name else {}
        async with uow:
            rarities = await self.rarities_repository.find_all(uow.session, **filter_by_dict)
            return rarities

    async def get_rarity(self, uow: IUnitOfWork, uuid: UUID):
        async with uow:
            rarity = await self.rarities_repository.find_one(uow.session, uuid=uuid)
            return rarity

    async def add_rarity(self, uow: IUnitOfWork, rarity: RarityCreate):
        async with uow:
            rarity_dict = {
                'uuid': rarity.uuid,
                'name': rarity.name,
                'color': rarity.color
            }
            await self.rarities_repository.add_one(uow.session, rarity_dict)
            await uow.commit()

    async def update_rarity(self, uow: IUnitOfWork, rarity: RarityUpdate):
        async with uow:
            rarity_dict = {
                'name': rarity.name,
                'color': rarity.color
            }
            await self.rarities_repository.edit_one(uow.session, rarity.uuid, rarity_dict)
            await uow.commit()

    async def delete_rarity(self, uow: IUnitOfWork, uuid: UUID):
        async with uow:
            await self.rarities_repository.delete_one(uow.session, uuid)
            await uow.commit()
