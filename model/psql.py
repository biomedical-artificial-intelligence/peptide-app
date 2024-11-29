import os
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)
Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def check_db():
    try:
        with engine.connect() as connection:
            connection.execute(text("SET search_path TO pipeline_simple"))
            result = await connection.execute(text("SELECT * FROM pipeline"))
            return result
    except Exception as e:
        raise Exception(status_code=500, detail=f"Database connection error: {str(e)}")