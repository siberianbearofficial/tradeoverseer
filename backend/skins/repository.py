from utils.repository import SQLAlchemyRepository

from .models import Skin


class SkinsRepository(SQLAlchemyRepository):
    model = Skin
