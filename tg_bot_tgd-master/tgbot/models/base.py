from sqlalchemy import make_url, create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, Session, sessionmaker
from ..config import load_config


def create_pool(config) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(
        url=make_url(
            f"postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.database}"
                     )
    )
    pool: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
    return pool


def create_session(config):
    engine = create_engine(
        f"postgresql+psycopg2://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.database}"
    )
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False,)
    return Session()


def sqlite_connect():
    engine = create_engine('sqlite:///./db.sqlite/', echo=True)
    Session = sessionmaker(bind=engine)
    return Session()


conf = load_config()

# engine = create_engine('sqlite:///./db.sqlite/', echo=True)
# session = sqlite_connect()
session = create_session(conf)
# async_session = create_pool(conf)
# async_session = async_session()
