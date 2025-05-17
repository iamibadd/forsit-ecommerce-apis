from fastapi import APIRouter, Query, Path
from typing import Annotated

from app.dependencies import SessionDep, PaginationDep, PaginatedDateFilterDep
from app.crud import sales as sales_crud
from app.schemas.sales import Sales, SalesProducts, SalesProductCategory, SalesStatsMetric


router = APIRouter(prefix="/sales", tags=["Sales"])


@router.get("", response_model=list[Sales])
def get_sales(
    db: SessionDep,
    filter: PaginationDep,
):
    sales = sales_crud.get_sales(db=db, filter=filter)
    return sales


@router.get("/by-date-range", response_model=list[Sales])
def get_sales_by_date_range(
    db: SessionDep,
    filter: PaginatedDateFilterDep,
):
    sales = sales_crud.get_sales_by_date_range(db=db, filter=filter)
    return sales


@router.get("/stats", response_model=dict)
def get_sales_stats(
    db: SessionDep,
    filter: Annotated[SalesStatsMetric, Query(description="Filter by different metrics")],
):
    stats = sales_crud.get_sales_stat(db=db, filter=filter)
    return {filter.metric: stats}


@router.get("/{sales_id}", response_model=Sales)
def get_sale_by_id(
    db: SessionDep,
    sales_id: Annotated[int, Path(description="Filter by sales id")],
):
    sale = sales_crud.get_sale_by_id(db=db, sales_id=sales_id)
    return sale


@router.get("/product/{product_id}", response_model=list[Sales])
def get_sales_by_product(
    db: SessionDep,
    product_id: Annotated[int, Path(description="Filter by product id")],
    filter: PaginationDep,
):
    sales = sales_crud.get_sales_by_product(
        db=db, product_id=product_id, filter=filter)
    return sales


@router.get("/product/{product_id}/details", response_model=list[SalesProducts])
def get_sales_by_product_details(
    db: SessionDep,
    product_id: Annotated[int, Path(description="Filter by product id")],
    filter: PaginationDep,
):
    sales = sales_crud.get_sales_by_product_details(
        db=db, product_id=product_id, filter=filter)
    return sales


@router.get("/category/{category_id}", response_model=list[Sales])
def get_sales_by_category(
    db: SessionDep,
    category_id: Annotated[int, Path(description="Filter by category id")],
    filter: PaginationDep,
):
    sales = sales_crud.get_sales_by_category(
        db=db, category_id=category_id, filter=filter)
    return sales


@router.get("/category/{category_id}/details", response_model=list[SalesProductCategory])
def get_sales_by_category_details(
    db: SessionDep,
    category_id: Annotated[int, Path(description="Filter by category id")],
    filter: PaginationDep,
):
    sales = sales_crud.get_sales_by_category_details(
        db=db, category_id=category_id, filter=filter)
    return sales
