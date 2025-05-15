from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    is_admin: bool | None = True


class UserLogin(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True
