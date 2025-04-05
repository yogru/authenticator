from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.infra.persistence.sqlalchemy.base_entity import BaseEntity


class UserAuthEntity(BaseEntity):
    __tablename__ = "user_auth"
    username = Column(String(255), nullable=False)
    password = Column(String(255), default=None, nullable=True)
    tokens = relationship("UserAuthTokenEntity", back_populates="user", cascade="all, delete-orphan")
    services = relationship("UserAuthServiceEntity", back_populates="user", cascade="all, delete-orphan")

    def deactivate_all_tokens(self):
        for token in self.tokens:
            token.deactivate()

    def create_token(self,
                     access_token: str,
                     refresh_token: str
                     ) -> "UserAuthTokenEntity":
        ret = UserAuthTokenEntity(
            user_id=self.id,
            access_token=access_token,
            refresh_token=refresh_token,
        )
        self.tokens.append(ret)
        return ret

    def sync_service(self, service_name) -> "UserAuthServiceEntity":
        for service in self.services:
            if service.name == service_name:
                return service

        ret = UserAuthServiceEntity(
            user_id=self.id,
            service_name=service_name
        )

        self.services.append(ret)
        return ret


class UserAuthServiceEntity(BaseEntity):
    __tablename__ = "user_auth_service"
    user_id = Column(ForeignKey("user_auth.id"), nullable=False)
    user = relationship("UserAuthEntity", back_populates="services")
    service_name = Column(String(256), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    deactivate_reason = Column(String(512), nullable=True)


class UserAuthTokenEntity(BaseEntity):
    __tablename__ = "user_auth_token"
    user_id = Column(ForeignKey("user_auth.id"), nullable=False)
    access_token = Column(String(512), nullable=False)
    refresh_token = Column(String(512), nullable=False)
    active = Column(Boolean, default=True, nullable=False)

    user = relationship("UserAuthEntity", back_populates="tokens")

    def deactivate(self):
        self.active = False
