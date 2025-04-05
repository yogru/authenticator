from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.repository.user_auth_repository import UserAuthRepository
from src.infra.persistence.sqlalchemy.base_entity import BaseEntity, BaseNoPkEntity
from src.infra.persistence.unit_of_work import AbstractAsyncUnitOfWork


class AsyncSqlAlchemyUow(AbstractAsyncUnitOfWork):
    def __init__(self, session_factory):
        """
        session_factory: async_sessionmaker(...) 또는 그와 유사한 함수.
        """
        self.session_factory = session_factory
        self.session: AsyncSession | None = None

    async def __aenter__(self):
        """
        비동기 컨텍스트 진입 시점에 세션을 열고, 필요한 Repository 인스턴스들을 준비합니다.
        """
        self.session = self.session_factory()  # type: AsyncSession
        self.user_auth_repository = UserAuthRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        """
        컨텍스트를 빠져나갈 때, 일단 rollback()을 호출하고
        세션을 종료(close)합니다.
        """
        await super().__aexit__(*args)
        await self.rollback()
        if self.session is not None:
            await self.session.close()

    def add(self, entity: Union[BaseEntity, BaseNoPkEntity]):
        self.session.add(entity)

    async def commit(self):
        """
        트랜잭션 커밋
        """
        if self.session is not None:
            await self.session.commit()

    async def rollback(self):
        """
        트랜잭션 롤백
        """
        if self.session is not None:
            await self.session.rollback()

    async def flush(self):
        """
        세션 flush
        """
        if self.session is not None:
            await self.session.flush()

    async def detach_from_persistence(self):
        """
        세션에 의해 관리되고 있는 객체들(Identity Map)과의 연결을 끊음
        (expunge_all 등)
        """
        if self.session is not None:
            self.session.expunge_all()
