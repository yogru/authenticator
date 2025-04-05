from typing import List, Optional, Generic, TypeVar, Any, Sequence, Type, Union
from uuid import UUID

from sqlalchemy import select, Select, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.persistence.sqlalchemy.base_entity import BaseEntity

# 엔티티 타입을 제네릭으로 받기 위한 설정
T = TypeVar("T")


class AsyncSqlAlchemyBaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        """
        :param session: 비동기용 SQLAlchemy 세션 (AsyncSession)
        :param model: 관리할 엔티티 클래스 (예: User, FAQ 등)
        """
        self.session = session
        self.model = model

    async def add(self, model: T) -> T:
        """
        엔티티 1건을 세션에 추가합니다.
        (commit/flush은 UoW나 호출부에서 수행)
        """
        self.session.add(model)
        return model

    async def add_all(self, models: List[T]):
        """
        엔티티 여러 건을 세션에 추가합니다.
        """
        self.session.add_all(models)

    async def delete(self, model: T):
        """
        엔티티 1건을 삭제 예정 상태로 만듭니다.
        (commit/flush은 UoW나 호출부에서 수행)
        """
        # 주의: delete()는 실제 삭제가 아니라,
        # flush/commit 시점에 반영됩니다.
        await self.session.delete(model)

    async def get(self, pk: UUID) -> Optional[T]:
        """
        기본키(pk)에 해당하는 엔티티 1건을 조회합니다.
        없으면 None을 반환합니다.
        """
        stmt = select(self.model).where(self.model.id == pk)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def fetch_one(self, stmt) -> Optional[T]:
        """
        SELECT 쿼리를 실행한 뒤, 단일 결과(또는 None)를 리턴한다.
        """
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def fetch_all(self, stmt) -> Sequence[Union[Row[Any], RowMapping, Any]]:
        """
        SELECT 쿼리를 실행한 뒤, 결과를 모두 리턴한다.
        """
        result = await self.session.execute(stmt)
        return result.scalars().all()
