import uuid
from sqlalchemy.orm import declarative_base

from sqlalchemy import Column, DateTime, func, Boolean
from sqlalchemy.dialects.postgresql import UUID

base_table = declarative_base()

class BaseNoPkEntity(base_table):
    __abstract__ = True  # 이 클래스는 테이블이 생성되지 않도록 설정 (추상 클래스)

    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.timezone('Asia/Seoul', func.now()), nullable=False)
    updated_at = Column(DateTime, server_default=func.timezone('Asia/Seoul', func.now()),
                        onupdate=func.timezone('Asia/Seoul', func.now()), nullable=False)

    def setup_delete(self, to_delete: bool = True):
        self.deleted = to_delete


class BaseEntity(base_table):
    __abstract__ = True  # 이 클래스는 테이블이 생성되지 않도록 설정 (추상 클래스)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.timezone('Asia/Seoul', func.now()), nullable=False)
    updated_at = Column(DateTime, server_default=func.timezone('Asia/Seoul', func.now()),
                        onupdate=func.timezone('Asia/Seoul', func.now()), nullable=False)

    def setup_delete(self, to_delete: bool = True):
        self.deleted = to_delete
