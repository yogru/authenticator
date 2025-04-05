import logging
from typing import Tuple

from sqlalchemy import create_engine, Engine, text, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, Session

from src.infra.env import EnvSettings
from src.infra.persistence.sqlalchemy.base_entity import base_table

logging.basicConfig()
logger = logging.getLogger(__name__)



def create_persistence(env: EnvSettings) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    """
     비동기 엔진과 비동기 세션을 반환
    """
    logging.getLogger("sqlalchemy").setLevel(logging.ERROR)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.ERROR)
    async_engine = create_async_engine(
        env.get_async_postgres_url(),
        echo=False
    )
    session_maker = async_sessionmaker(async_engine, expire_on_commit=False)
    return async_engine, session_maker


def create_persistence_sync_engine(env: EnvSettings) -> Engine:
    engine = create_engine(
        env.get_postgres_url(),  # sync용 URL
        echo=True
    )
    return engine


def create_tables(env: EnvSettings):
    # 사고 방지..
    if env.ENV_TYPE == "prod":
        logger.info("Production mode - Create Tables aborted!")
        return
    engine = create_persistence_sync_engine(env)
    base_table.metadata.create_all(engine)


def drop_truncate_tables(env: EnvSettings, only_truncate: bool = False):
    if env.ENV_TYPE == "prod":
        logger.info("Production mode - Truncate and Drop aborted!")
        return
    engine = create_persistence_sync_engine(env)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    sm = sessionmaker(bind=engine)
    session = sm()
    # 모든 테이블 순서대로 튜런케이트 후 드롭
    with engine.connect() as conn:
        trans = conn.begin()  # 트랜잭션 시작
        try:
            # 외래 키 무시 (필요한 경우)
            conn.execute(text('SET session_replication_role = replica;'))
            for table in reversed(metadata.sorted_tables):
                conn.execute(text(f"TRUNCATE TABLE {table.name} CASCADE;"))
                if only_truncate:
                    continue
                conn.execute(text(f"DROP TABLE {table.name} CASCADE;"))
            conn.execute(text('SET session_replication_role = DEFAULT;'))  # 외래 키 검사를 다시 활성화
            trans.commit()
        except Exception as e:
            trans.rollback()
            logger.info(f"Error occurred: {e}")
            raise
        finally:
            session.close()


def drop_tables(env: EnvSettings):
    drop_truncate_tables(env=env)


def truncate_tables(env: EnvSettings):
    drop_truncate_tables(env=env, only_truncate=True)
