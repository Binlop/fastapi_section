from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

async_engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/dbname")

AsyncSession = async_sessionmaker(expire_on_commit=False, bind=async_engine)

async def get_async_db():
    async with AsyncSession() as session:
        yield session