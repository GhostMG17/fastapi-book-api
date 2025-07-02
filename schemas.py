from pydantic import BaseModel, Field


# 📚 Схема для добавления книги (входные данные)
class BookCreate(BaseModel):
    title: str = Field(..., example="1984", description="Название книги")
    author: str = Field(..., example="George Orwell", description="Имя автора")


# 📖 Схема для чтения книги (ответ клиенту), включает id
class BookRead(BookCreate):
    id: int = Field(..., example=1, description="ID книги")


# 👤 Схема для регистрации пользователя
class UserCreate(BaseModel):
    username: str = Field(..., example="johndoe", description="Имя пользователя")
    password: str = Field(..., example="strongpassword123", min_length=6, description="Пароль (не менее 6 символов)")


# 👤 Схема для ответа (без пароля)
class UserRead(BaseModel):
    id: int = Field(..., example=1, description="ID пользователя")
    username: str = Field(..., example="johndoe", description="Имя пользователя")


# 🔑 Схема токена при логине
class Token(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field(default="bearer", example="bearer")
