from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.domain.model.user_auth_entity import UserAuthEntity
from src.infra.persistence.sqlalchemy.async_base_repository import AsyncSqlAlchemyBaseRepository


class UserAuthRepository(AsyncSqlAlchemyBaseRepository[UserAuthEntity]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserAuthEntity)

    async def get_user_by_username(self, username: str) -> Optional[UserAuthEntity]:
        stmt = (
            select(UserAuthEntity)
            .options(selectinload(UserAuthEntity.tokens),
                     selectinload(UserAuthEntity.services)
                     )  # 관계 이름에 맞게!
            .where(UserAuthEntity.username == username)
        )
        return await self.fetch_one(stmt)
