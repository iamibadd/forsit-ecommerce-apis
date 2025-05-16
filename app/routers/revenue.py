from fastapi import APIRouter

from app.dependencies import SessionDep, PaginationDep, PaginatedDateFilterDep
from app.crud import revenue as revenue_crud
from app.schemas.revenue import Revenue


router = APIRouter(prefix="/revenue", tags=["Revenue"])


@router.get("", response_model=list[Revenue])
def get_revenue(
    db: SessionDep,
    filter: PaginationDep,
):
    revenue = revenue_crud.get_revenue(db=db, filter=filter)
    return revenue


@router.get("/by_date_range", response_model=list[Revenue])
def get_revenue_by_date_range(
    db: SessionDep,
    filter: PaginatedDateFilterDep,
):
    revenue = revenue_crud.get_revenue_by_date_range(db=db, filter=filter)
    return revenue
