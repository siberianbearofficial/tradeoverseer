from utils.repository import SQLAlchemyRepository

from .models import Rarity


class RaritiesRepository(SQLAlchemyRepository):
    model = Rarity
