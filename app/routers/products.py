from fastapi import APIRouter
from app.dependencies import UserDep

router = APIRouter()


@router.get("")
def get_products(user: UserDep):
    return {
        "message": f"Hello {user.email}, here are your products."
    }
