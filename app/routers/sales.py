from fastapi import APIRouter, Query, Path
from typing import Annotated
from datetime import datetime

from app.dependencies import SessionDep, PaginationDep
from app.crud import sales as sales_crud
from app.schemas.sales import Sales, SalesProducts, SalesProductCategory


router = APIRouter()


@router.get("", response_model=list[Sales])
def get_sales(
    db: SessionDep,
    pagination: PaginationDep,
):
    sales = sales_crud.get_sales(db=db, pagination=pagination)
    return sales


@router.get("/by_date_range", response_model=list[Sales])
def get_sales_by_date_range(
    db: SessionDep,
    start_date: Annotated[datetime, Query(description="Enter the start date to filter")],
    end_date: Annotated[datetime, Query(description="Enter the end date to filter")],
    pagination: PaginationDep,
):
    sales = sales_crud.get_sales_by_date_range(
        db=db, start_date=start_date, end_date=end_date, pagination=pagination)
    return sales


@router.get("/product/{product_id}", response_model=list[Sales])
def get_sales_by_product(
    db: SessionDep,
    product_id: Annotated[int, Path(description="Filter by product id")],
    pagination: PaginationDep,
):
    sales = sales_crud.get_sales_by_product(
        db=db, product_id=product_id, pagination=pagination)
    return sales


@router.get("/product/{product_id}/details", response_model=list[SalesProducts])
def get_sales_by_product_details(
    db: SessionDep,
    product_id: Annotated[int, Path(description="Filter by product id")],
    pagination: PaginationDep,
):
    sales = sales_crud.get_sales_by_product_details(
        db=db, product_id=product_id, pagination=pagination)
    return sales


@router.get("/category/{category_id}", response_model=list[Sales])
def get_sales_by_category(
    db: SessionDep,
    category_id: Annotated[int, Path(description="Filter by category id")],
    pagination: PaginationDep,
):
    sales = sales_crud.get_sales_by_category(
        db=db, category_id=category_id, pagination=pagination)
    return sales


@router.get("/category/{category_id}/details", response_model=list[SalesProductCategory])
def get_sales_by_category_details(
    db: SessionDep,
    category_id: Annotated[int, Path(description="Filter by category id")],
    pagination: PaginationDep,
):
    sales = sales_crud.get_sales_by_category_details(
        db=db, category_id=category_id, pagination=pagination)
    return sales
