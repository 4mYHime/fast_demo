from contextlib import contextmanager
from typing import Generator
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from aioredis import create_redis_pool, Redis
from setting import settings

engine = create_engine(settings.MYSQL_SQLALCHEMY_DB_URI,
                       echo=False,
                       pool_size=200,
                       pool_recycle=120,
                       max_overflow=200,
                       pool_pre_ping=True
                       )

Session = scoped_session(
    sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=True,
        autocommit=False
    )
)


# 实例化session
def get_session():
    return Session()


@contextmanager
def get_dbs() -> Generator:
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_db() -> Generator:
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


async def get_redis_pool() -> Redis:
    redis = await create_redis_pool(settings.REDIS_URL)
    return redis
