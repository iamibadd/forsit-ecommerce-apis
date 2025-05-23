from app.models.users import User
from fastapi import Depends, Query, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated, Optional
from sqlmodel import Session
from datetime import date
from app.database.session import get_db
from app.crud.users import get_user_by_email
from app.utils.auth import verify_access_token
from app.schemas.users import UserResponse
from app.schemas.helpers import Pagination, PaginatedDateFilter, DateFilter


class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        if not authorization or not authorization.lower().startswith("bearer"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="A bearer token is required in the header.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return await super().__call__(request)


oauth2_scheme = CustomOAuth2PasswordBearer(tokenUrl="/v2/api/auth/login")

SessionDep = Annotated[Session, Depends(get_db)]

TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(
    db: SessionDep,
    token: TokenDep,
) -> UserResponse:
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication token")

    email = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = get_user_by_email(db=db, email=email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User is not admin")

    return user


UserDep = Annotated[User, Depends(get_current_user)]


def pagination_params(
    offset: int = Query(0, description="Offset for pagination"),
    limit: int = Query(100, description="Limit for pagination"),
) -> Pagination:
    return Pagination(offset=offset, limit=limit)


PaginationDep = Annotated[Pagination, Depends(pagination_params)]


def paginated_date_filter_params(
    offset: int = Query(0, description="Offset for pagination"),
    limit: int = Query(100, description="Limit for pagination"),
    start_date: date = Query(..., description="Start date for filtering"),
    end_date: date = Query(..., description="End date for filtering"),
) -> PaginatedDateFilter:
    return PaginatedDateFilter(
        offset=offset, limit=limit, start_date=start_date, end_date=end_date
    )


PaginatedDateFilterDep = Annotated[PaginatedDateFilter, Depends(
    paginated_date_filter_params)]


def date_filter_params(
    start_date: date = Query(..., description="Start date for filtering"),
    end_date: date = Query(..., description="End date for filtering"),
) -> DateFilter:
    return DateFilter(
        start_date=start_date, end_date=end_date
    )


DateFilterDep = Annotated[DateFilter, Depends(
    paginated_date_filter_params)]
