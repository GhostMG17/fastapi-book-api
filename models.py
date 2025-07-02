from sqlalchemy.orm import Mapped, mapped_column,relationship
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey


# Определяем модель таблицы "books"
class Book(Base):
    __tablename__ = "books" # имя таблицы в БД

    id: Mapped[int] = mapped_column(primary_key=True)  # автоинкрементный ID
    title: Mapped[str] # название книги
    author: Mapped[str] # автор

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))  # связь с User
    owner: Mapped["User"] = relationship(back_populates="books")  # обратная связь


# 👤 Модель пользователя
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    hashed_password: Mapped[str]  # храним зашифрованный пароль

    books: Mapped[list["Book"]] = relationship(back_populates="owner")
