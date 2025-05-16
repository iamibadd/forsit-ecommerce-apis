from fastapi import HTTPException, status
from datetime import date
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.models import Sale, Product
from app.schemas.pagination import PaginationParams
from app.schemas.sales import SalesStatsMetric


def raise_not_found_if_empty(data: list, resource: str, resource_id: int, offset: int = 0):
    if not data and offset == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No {resource} found for {resource} ID {resource_id}"
        )


def get_sales(*, db: Session, pagination: PaginationParams) -> list[Sale]:
    return db.query(Sale).offset(pagination.offset).limit(pagination.limit).all()


def get_sale_by_id(*, db: Session, sales_id: int) -> Sale:
    sale = db.get(Sale, sales_id)
    raise_not_found_if_empty(sale, "sale", sales_id)
    return sale


def get_sales_stat(
    *,
    db: Session,
    params: SalesStatsMetric
) -> int | float:
    start_date = params.start_date
    end_date = params.end_date  # fixed here
    metric = params.metric

    query = db.query(Sale)

    if start_date and end_date:
        query = query.filter(Sale.sale_date.between(start_date, end_date))

    if metric == "total_sales":
        return query.count()

    condition = Sale.sale_date.between(
        start_date, end_date) if start_date and end_date else True

    if metric == "total_quantity":
        result = db.query(func.sum(Sale.quantity)).filter(
            condition).scalar()
        return int(result) if result is not None else 0

    if metric == "total_amount":
        result = db.query(func.sum(Sale.total_price)
                          ).filter(condition).scalar()
        return float(result) if result is not None else 0.0

    raise ValueError("Invalid metric specified")


def get_sales_by_date_range(*, db: Session, start_date: date, end_date: date,  pagination: PaginationParams) -> list[Sale]:
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
