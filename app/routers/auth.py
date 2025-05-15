from fastapi import APIRouter, HTTPException
from app.dependencies import SessionDep
from app.schemas.users import UserLogin
from app.utils.users import verify_password
from app.utils.auth import create_access_token
from app.crud import users as user_crud

router = APIRouter()


@router.post("/login")
def login(user_credentials: UserLogin, db: SessionDep):
    user = user_crud.get_user_by_email(db=db, email=user_credentials.email)

    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=401, detail="Invalid email or password")

    token_data = {"sub": user.email, "is_admin": user.is_admin}
    token = create_access_token(data=token_data)

    return {"access_token": token, "token_type": "bearer"}
