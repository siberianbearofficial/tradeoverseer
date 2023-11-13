from utils.repository import SQLAlchemyRepository

from .models import InventoryItem


class InventoryRepository(SQLAlchemyRepository):
    model = InventoryItem
