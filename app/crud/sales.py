from fastapi import HTTPException
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from app.models import Sale, Product
from app.schemas.pagination import PaginationParams


def raise_not_found_if_empty(data: list, resource: str, resource_id: int, offset: int):
    if not data and offset == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No {resource} found for {resource} ID {resource_id}"
        )


def get_sales(*, db: Session, pagination: PaginationParams) -> list[Sale]:
    return db.query(Sale).offset(pagination.offset).limit(pagination.limit).all()


def get_sales_by_date_range(*, db: Session, start_date: datetime, end_date: datetime,  pagination: PaginationParams) -> list[Sale]:
    return db.query(Sale).filter(Sale.sale_date.between(start_date, end_date)).offset(pagination.offset).limit(pagination.limit).all()


def get_sales_by_product(*, db: Session, product_id: int, pagination: PaginationParams) -> list[Sale]:
    sales = db.query(Sale).filter(Sale.product_id == product_id).offset(
        pagination.offset).limit(pagination.limit).all()
    raise_not_found_if_empty(sales, "product", product_id, pagination.offset)
    return sales


def get_sales_by_product_details(*, db: Session, product_id: int, pagination: PaginationParams) -> list[Sale]:
    sales = db.query(Sale).options(joinedload(Sale.product)).filter(
        Sale.product_id == product_id).offset(pagination.offset).limit(pagination.limit).all()
    raise_not_found_if_empty(sales, "product", product_id, pagination.offset)
    return sales


def get_sales_by_category(*, db: Session, category_id: int, pagination: PaginationParams) -> list[Sale]:
    sales = db.query(Sale).join(Product).options(joinedload(Sale.product).joinedload(Product.category)).filter(
        Product.category_id == category_id).offset(pagination.offset).limit(pagination.limit).all()
    raise_not_found_if_empty(sales, "category", category_id, pagination.offset)
    return sales


def get_sales_by_category_details(*, db: Session, category_id: int, pagination: PaginationParams) -> list[Sale]:
    sales = db.query(Sale).join(Product).filter(Product.category_id == category_id).offset(
        pagination.offset).limit(pagination.limit).all()
    raise_not_found_if_empty(sales, "category", category_id, pagination.offset)
    return sales
