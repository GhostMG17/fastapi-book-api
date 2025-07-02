import os
import uuid
import pytest
import asyncio
from httpx import AsyncClient
from main import app, init_db  # 👈 импортируем init_db


# Удаляем файл базы данных перед запуском тестов
if os.path.exists("books.db"):
    os.remove("books.db")


@pytest.mark.asyncio
async def test_register_and_login():
    username = f"user_{uuid.uuid4().hex[:6]}"
    password = "secret"

    # Создаём таблицы
    await init_db()

    async with AsyncClient(app=app, base_url="http://test") as client:
        # Регистрация
        response = await client.post("/register", json={
            "username": username,
            "password": password
        })
        print("REGISTER:", response.status_code, response.text)
        assert response.status_code == 200
        assert response.json()["username"] == username

        # Логин
        response = await client.post("/login", data={
            "username": username,
            "password": password
        })
        print("LOGIN:", response.status_code, response.text)
        assert response.status_code == 200
        token = response.json()["access_token"]
        assert token

        # Проверка /me
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("/me", headers=headers)
        assert response.status_code == 200
        assert response.json()["username"] == username


@pytest.mark.asyncio
async def test_book_crud():
    await init_db()  # 👈 создаём таблицы

    async with AsyncClient(app=app, base_url="http://test") as client:
        # Пользователь A
        await client.post("/register", json={"username": "userA", "password": "123"})
        await asyncio.sleep(0.1)  # 👈 даём БД завершить commit
        login_a = await client.post("/login", data={"username": "userA", "password": "123"})

        print("LOGIN_A STATUS:", login_a.status_code)
        print("LOGIN_A BODY:", login_a.text)

        assert login_a.status_code == 200, login_a.text  # 👈 это важно

        token_a = login_a.json()["access_token"]
        headers_a = {"Authorization": f"Bearer {token_a}"}

        # Создание книги
        response = await client.post("/books", json={
            "title": "Моя книга",
            "author": "Автор A"
        }, headers=headers_a)
        assert response.status_code == 200
        book_id = response.json()["id"]

        # Получение книг A
        response = await client.get("/books", headers=headers_a)
        assert response.status_code == 200
        books = response.json()
        assert len(books) == 1
        assert books[0]["title"] == "Моя книга"

        # Пользователь B
        await client.post("/register", json={"username": "userB", "password": "123"})
        await asyncio.sleep(0.1)  # 👈 даём БД завершить commit
        login_b = await client.post("/login", data={"username": "userB", "password": "123"})
        token_b = login_b.json()["access_token"]
        headers_b = {"Authorization": f"Bearer {token_b}"}

        # B не видит книги A
        response = await client.get("/books", headers=headers_b)
        assert response.status_code == 200
        assert response.json() == []

        # B не может удалить книгу A
        response = await client.delete(f"/books/{book_id}", headers=headers_b)
        assert response.status_code == 404

        # A обновляет свою книгу
        response = await client.put(f"/books/{book_id}", json={
            "title": "Обновлённая книга",
            "author": "Автор A"
        }, headers=headers_a)
        assert response.status_code == 200
        assert response.json()["title"] == "Обновлённая книга"

        # A удаляет свою книгу
        response = await client.delete(f"/books/{book_id}", headers=headers_a)
        assert response.status_code == 200
        assert response.json()["detail"] == "Книга удалена"
