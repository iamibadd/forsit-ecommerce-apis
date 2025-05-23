from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.models import Sale, Product
from app.schemas.helpers import Pagination, PaginatedDateFilter
from app.schemas.sales import SalesStatsMetric
from app.helpers.if_empty import raise_not_found_if_empty


def get_sales(*, db: Session, filter: Pagination) -> list[Sale]:
    return db.query(Sale).offset(filter.offset).limit(filter.limit).all()


def get_sale_by_id(*, db: Session, sales_id: int) -> Sale:
    sale = db.get(Sale, sales_id)
    raise_not_found_if_empty("sale", sales_id, sale)
    return sale


def get_sales_stat(*, db: Session, filter: SalesStatsMetric) -> int | float:
    start_date = filter.start_date
    end_date = filter.end_date
    metric = filter.metric

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


def get_sales_by_date_range(*, db: Session, filter: PaginatedDateFilter) -> list[Sale]:
    return db.query(Sale).filter(Sale.sale_date.between(filter.start_date, filter.end_date)).offset(filter.offset).limit(filter.limit).all()


def get_sales_by_product(*, db: Session, product_id: int, filter: Pagination) -> list[Sale]:
    sales = db.query(Sale).filter(Sale.product_id == product_id).offset(
        filter.offset).limit(filter.limit).all()
    raise_not_found_if_empty("product", product_id, sales, filter.offset)
    return sales


def get_sales_by_product_details(*, db: Session, product_id: int, filter: Pagination) -> list[Sale]:
    sales = db.query(Sale).options(joinedload(Sale.product)).filter(
        Sale.product_id == product_id).offset(filter.offset).limit(filter.limit).all()
    raise_not_found_if_empty("product", product_id, sales, filter.offset)
    return sales


def get_sales_by_category(*, db: Session, category_id: int, filter: Pagination) -> list[Sale]:
    sales = db.query(Sale).join(Product).options(joinedload(Sale.product).joinedload(Product.category)).filter(
        Product.category_id == category_id).offset(filter.offset).limit(filter.limit).all()
    raise_not_found_if_empty("category", category_id, sales, filter.offset)
    return sales


def get_sales_by_category_details(*, db: Session, category_id: int, filter: Pagination) -> list[Sale]:
    sales = db.query(Sale).join(Product).filter(Product.category_id == category_id).offset(
        filter.offset).limit(filter.limit).all()
    raise_not_found_if_empty("category", category_id, sales, filter.offset)
    return sales
