import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.utils.config import get_env

DATABASE_URL = get_env("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)

Session = sessionmaker(
    bind=engine,
    autocommit=False,
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession,
)

Base = declarative_base()


async def get_db():
    async with Session() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_db_session():
    session = Session()
    return session


async def close_db_session(session):
    await session.close()
    

async def get_connection():
    """PostgreSQL 데이터베이스에 직접 연결하고 연결 객체를 반환"""
    conn = await asyncpg.connect(DATABASE_URL.replace('postgresql+asyncpg', 'postgresql'))
    return conn


async def close_connection(conn):
    """PostgreSQL 연결 종료"""
    await conn.close()