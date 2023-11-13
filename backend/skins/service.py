from uuid import UUID

from utils.unitofwork import IUnitOfWork

from .repository import SkinsRepository
from .schemas import SkinCreate, SkinUpdate


class SkinsService:
    def __init__(self, skins_repository: SkinsRepository):
        self.skins_repository = skins_repository

    async def get_skins(self, uow: IUnitOfWork, name: str | None = None):
        filter_by_dict = {'name': name} if name else {}
        async with uow:
            skins = await self.skins_repository.find_all(uow.session, **filter_by_dict)
            return skins

    async def get_skin(self, uow: IUnitOfWork, uuid: UUID):
        async with uow:
            skin = await self.skins_repository.find_one(uow.session, uuid=uuid)
            return skin

    async def add_skin(self, uow: IUnitOfWork, skin: SkinCreate):
        async with uow:
            skin_dict = {
                'uuid': skin.uuid,
                'name': skin.name,
                'rarity_uuid': skin.rarity_uuid
            }
            await self.skins_repository.add_one(uow.session, skin_dict)
            await uow.commit()

    async def update_skin(self, uow: IUnitOfWork, skin: SkinUpdate):
        async with uow:
            skin_dict = {
                'name': skin.name,
                'rarity_uuid': skin.rarity_uuid
            }
            await self.skins_repository.edit_one(uow.session, skin.uuid, skin_dict)
            await uow.commit()

    async def delete_skin(self, uow: IUnitOfWork, uuid: UUID):
        async with uow:
            await self.skins_repository.delete_one(uow.session, uuid)
            await uow.commit()
