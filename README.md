# 📚 Book API — FastAPI приложение с авторизацией

![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-brightgreen?logo=fastapi)
![Dockerized](https://img.shields.io/badge/Docker-ready-blue?logo=docker)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📌 Описание

**Book API** — это RESTful API на FastAPI, позволяющее пользователям:
- Регистрироваться и авторизовываться через JWT
- Управлять своими книгами (добавлять, просматривать, редактировать, удалять)
- Работать с асинхронной базой данных (SQLite через SQLAlchemy)
- Писать автотесты (pytest + httpx)
- Запускать приложение в Docker-контейнере

---

## ⚙️ Используемые технологии

- 🐍 Python 3.11+
- ⚡ FastAPI
- 🔐 JWT (OAuth2 + Bearer)
- 🛢️ SQLAlchemy 2.x (async)
- 🧂 passlib + bcrypt
- 🐳 Docker
- ✅ pytest + httpx

---

## 🚀 Запуск локально

### 1. Клонируй репозиторий

```bash
git clone https://github.com/username/fastapi-book-api.git
cd fastapi-book-api
```
### 2. Установи зависимости и запусти сервер
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Документация API
```bash
Открой в браузере:

Swagger: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc
```

### 🐳 Docker (простой запуск)
```bash
docker build -t fastapi-books .
docker run -it --rm -p 8000:8000 fastapi-books
```

### 🧪 Запуск тестов
``` bash
pytest test_main.py
```

### 📬 Примеры API
#### Регистрация
``` bash
POST /register
{
  "username": "admin",
  "password": "secret"
}
```

#### Логин
``` bash
POST /login
Form: username=admin&password=secret
Returns: {"access_token": "…"}
```

#### Добавление книги
``` bash
POST /books
Headers: Authorization: Bearer <token>
{
  "title": "Моя книга",
  "author": "Я"
}
```

### 📁 Структура проекта
``` bash
.
├── main.py              # Основное приложение FastAPI
├── models.py            # SQLAlchemy модели
├── schemas.py           # Pydantic схемы
├── auth.py              # Хэширование, JWT, безопасность
├── database.py          # Настройка базы данных
├── test_main.py         # Автотесты
├── Dockerfile           # Docker-образ
└── requirements.txt     # Зависимости
```

