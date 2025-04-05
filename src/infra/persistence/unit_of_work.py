import abc
from typing import Union

from src.infra.persistence.sqlalchemy.base_entity import BaseEntity, BaseNoPkEntity


class AbstractAsyncUnitOfWork(abc.ABC):
    """
    비동기 Unit of Work 인터페이스
    """

    async def __aenter__(self) -> "AbstractAsyncUnitOfWork":
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    @abc.abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def flush(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def detach_from_persistence(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, entity: Union[BaseEntity, BaseNoPkEntity]):
        raise NotImplementedError
