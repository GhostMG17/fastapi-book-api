from fastapi import FastAPI, Depends, HTTPException, status, Path
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth import hash_password, verify_password, create_access_token, get_current_user
from models import Book, User
from schemas import BookCreate, BookRead, UserCreate, UserRead, Token
from database import engine, Base, get_session


# Создаём FastAPI-приложение
app = FastAPI(
    title="📚 Book API",
    description="API для управления книгами пользователей с авторизацией по JWT.",
    version="1.0.0"
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# При старте приложения — создаём таблицы (если их нет)
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post(
    "/register",
    response_model=UserRead,
    tags=["Auth"],
    summary="Регистрация нового пользователя",
    description="Создаёт нового пользователя и сохраняет хешированный пароль в базе данных."
)
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    # Проверка: есть ли такой пользователь
    existing = await session.execute(
        select(User).where(User.username == user.username)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    # Хешируем пароль и создаём нового пользователя
    new_user = User(
        username=user.username,
        hashed_password=hash_password(user.password)
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@app.post(
    "/login",
    response_model=Token,
    tags=["Auth"],
    summary="Аутентификация пользователя",
    description="Проверяет логин и пароль. Возвращает JWT-токен для доступа к защищённым маршрутам."
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    # Генерируем токен
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


# POST /books — добавить новую книгу
@app.post(
    "/books",
    response_model=BookRead,
    tags=["Books"],
    summary="Добавить новую книгу",
    description="Создаёт новую книгу, привязанную к текущему авторизованному пользователю."
)
async def create_book(
    book: BookCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    new_book = Book(  # создаём объект книги
        title=book.title,
        author=book.author,
        owner_id=current_user.id
    )
    session.add(new_book)  # добавляем в сессию
    await session.commit()  # сохраняем в базе
    await session.refresh(new_book)  # обновляем из базы, чтобы получить id
    return new_book  # возвращаем клиенту


# GET /books — получить список всех книг
@app.get(
    "/books",
    response_model=list[BookRead],
    tags=["Books"],
    summary="Получить список книг",
    description="Возвращает список всех книг, принадлежащих текущему пользователю."
)
async def list_books(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    result = await session.execute(
        select(Book).where(Book.owner_id == current_user.id)
    )  # делаем SELECT * FROM books
    return result.scalars().all()  # возвращаем список книг


@app.get(
    "/me",
    response_model=UserRead,
    tags=["Auth"],
    summary="Информация о текущем пользователе",
    description="Возвращает информацию о текущем авторизованном пользователе."
)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@app.delete(
    "/books/{book_id}",
    response_model=dict,
    tags=["Books"],
    summary="Удалить книгу",
    description="Удаляет книгу по ID, если она принадлежит текущему пользователю."
)
async def delete_book(
    book_id: int = Path(..., gt=0),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Ищем книгу по ID и проверяем владельца
    result = await session.execute(
        select(Book).where(Book.id == book_id, Book.owner_id == current_user.id)
    )
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена или не принадлежит вам")

    await session.delete(book)
    await session.commit()
    return {"detail": "Книга удалена"}


@app.put(
    "/books/{book_id}",
    response_model=BookRead,
    tags=["Books"],
    summary="Обновить книгу",
    description="Обновляет заголовок и автора книги по ID, если книга принадлежит текущему пользователю."
)
async def update_book(
    book_id: int = Path(..., gt=0),
    data: BookCreate = Depends(),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Ищем книгу по ID и владельцу
    result = await session.execute(
        select(Book).where(Book.id == book_id, Book.owner_id == current_user.id)
    )
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена или не принадлежит вам")

    # Обновляем поля
    book.title = data.title
    book.author = data.author

    await session.commit()
    await session.refresh(book)
    return book
