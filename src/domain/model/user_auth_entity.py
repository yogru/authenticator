from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.infra.persistence.sqlalchemy.base_entity import BaseEntity


class UserAuthEntity(BaseEntity):
    __tablename__ = "user_auth"
    username = Column(String(255), nullable=False)
    password = Column(String(255), default=None, nullable=True)
    refresh_token = Column(String(512), nullable=True, default=None)
    services = relationship("UserAuthServiceEntity", back_populates="user", cascade="all, delete-orphan")

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

    def check_service(self, service_name) -> bool:
        for service in self.services:
            if service.service_name == service_name:
                return True
        return False

    def setup_refresh_token(self, refresh_token: str) -> str:
        pre_refresh_token = self.refresh_token
        self.refresh_token = refresh_token
        return pre_refresh_token


class UserAuthServiceEntity(BaseEntity):
    __tablename__ = "user_auth_service"
    user_id = Column(ForeignKey("user_auth.id"), nullable=False)
    user = relationship("UserAuthEntity", back_populates="services")
    active = Column(Boolean, default=True, nullable=False)
    service_name = Column(String(256), nullable=False)
    deactivate_reason = Column(String(512), nullable=True)
