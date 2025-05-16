from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    password: str = Field(max_length=255)
    is_admin: bool = True


class User(UserBase, table=True):
    __tablename__ = 'users'

    id: int | None = Field(default=None, primary_key=True, index=True)
