from abc import ABC, abstractmethod

from .database import async_session_maker


class IUnitOfWork(ABC):

    @abstractmethod
    def __init__(self):
        self.session_factory = None

    @abstractmethod
    async def __aenter__(self):
        self.session = None

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

    async def __aexit__(self, *args):
        # await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
