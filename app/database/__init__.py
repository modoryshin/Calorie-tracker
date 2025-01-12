from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.database import models

URL_DATABASE = 'sqlite+aiosqlite:///db.sqlite'

engine = create_async_engine(url=URL_DATABASE)

async_session = async_sessionmaker(autoflush=False, bind=engine)

async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

    db = async_session()
    try:
        yield db
    finally:
        await db.close()