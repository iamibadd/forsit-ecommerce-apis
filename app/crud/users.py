from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.users import UserCreate, UserResponse
from app.models import User
from app.utils.users import hash_password


def create_user(*, db: Session, user: UserCreate) -> UserResponse:
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    updated_fields = {"password": hashed_password}
    new_user = User.model_validate(user, update=updated_fields)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_email(*, db: Session, email: str) -> UserCreate:
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Email does not exist")
    return db_user
