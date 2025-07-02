from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# URL подключения к базе (SQLite через aiosqlite)
DATABASE_URL = "sqlite+aiosqlite:///./books.db"

# Создаём асинхронный движок SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаём фабрику сессий — то, через что мы обращаемся к БД
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Функция-зависимость для FastAPI — отдаёт сессию
async def get_session():
    async with SessionLocal() as session:
        yield session

# Базовый класс для моделей
class Base(DeclarativeBase):
    pass



