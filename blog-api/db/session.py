from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import DateTime, func
from core.config import settings
from datetime import datetime, timezone

async_engine = create_async_engine(settings.DATABASE_URL)

AsyncSession = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)

def utcnow():
    return datetime.now(timezone.utc)

class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

async def get_async_db():
    async with AsyncSession() as session:
        yield session