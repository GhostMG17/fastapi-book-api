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
