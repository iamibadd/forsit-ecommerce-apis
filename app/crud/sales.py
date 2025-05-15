from fastapi import HTTPException
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from app.models import Sale, Product
from app.schemas.pagination import PaginationParams


def get_sales(*, db: Session, pagination: PaginationParams) -> list[Sale]:
    return db.query(Sale).offset(pagination.offset).limit(pagination.limit).all()


def get_sales_by_date_range(*, db: Session, start_date: datetime, end_date: datetime,  pagination: PaginationParams) -> list[Sale]:
    return db.query(Sale).filter(Sale.sale_date.between(start_date, end_date)).offset(pagination.offset).limit(pagination.limit).all()


def get_sales_by_product(*, db: Session, product_id: int, pagination: PaginationParams) -> list[Sale]:
    sales = db.query(Sale).filter(Sale.product_id == product_id).offset(
        pagination.offset).limit(pagination.limit).all()
    if not sales and pagination.offset == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No sales found for product ID {product_id}"
        )
    return sales


def get_sales_by_product_details(*, db: Session, product_id: int, pagination: PaginationParams) -> list[Sale]:
    sales = db.query(Sale).options(joinedload(Sale.product)).filter(
        Sale.product_id == product_id).offset(pagination.offset).limit(pagination.limit).all()
    if not sales and pagination.offset == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No sales found for product ID {product_id}"
        )
    return sales


def get_sales_by_category(*, db: Session, category_id: int, pagination: PaginationParams) -> list[Sale]:
    sales = db.query(Sale).join(Product).options(joinedload(Sale.product).joinedload(Product.category)).filter(
        Product.category_id == category_id).offset(pagination.offset).limit(pagination.limit).all()
    if not sales and pagination.offset == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No sales found for category ID {category_id}"
        )
    return sales


def get_sales_by_category_details(*, db: Session, category_id: int, pagination: PaginationParams) -> list[Sale]:
    sales = db.query(Sale).join(Product).filter(Product.category_id == category_id).offset(
        pagination.offset).limit(pagination.limit).all()
    if not sales and pagination.offset == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No sales found for category ID {category_id}"
        )
    return sales
