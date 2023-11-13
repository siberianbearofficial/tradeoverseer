from utils.repository import SQLAlchemyRepository

from .models import Role


class RolesRepository(SQLAlchemyRepository):
    model = Role
