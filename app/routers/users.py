from fastapi import APIRouter
from app.dependencies import SessionDep
from app.schemas.users import UserCreate, UserResponse
from app.crud import users as user_crud


router = APIRouter()


@router.post("", response_model=UserResponse)
def create_user(user_body: UserCreate, db: SessionDep):
    user = user_crud.create_user(db=db, user=user_body)
    return user
