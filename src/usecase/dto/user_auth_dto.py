from uuid import UUID

from pydantic import BaseModel

from src.domain.model.user_auth_entity import UserAuthEntity


class SimpleUserAuthDto(BaseModel):
    id: UUID
    username: str

    @staticmethod
    def of(entity: UserAuthEntity) -> 'SimpleUserAuthDto':
        return SimpleUserAuthDto(
            id=entity.id,
            username=entity.username
        )
