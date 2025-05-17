from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.models import Product, Category
from app.schemas.helpers import Pagination
from app.schemas.products import ProductCreate, ProductStatsMetric
from app.helpers.if_empty import raise_not_found_if_empty


def create_product(*, db: Session, product: ProductCreate) -> Product:
    category = db.get(Category, product.category_id)
    raise_not_found_if_empty("category", product.category_id, category)
    db_product = Product.model_validate(product)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_products(*, db: Session, filter: Pagination, name: str | None = None, description: str | None = None) -> list[Product]:
    query = db.query(Product)
    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    if description:
        query = query.filter(Product.description.ilike(f"%{description}%"))
    products = query.offset(offset=filter.offset).limit(
        limit=filter.limit).all()
    return products


def get_product_by_id(*, db: Session, product_id: int) -> Product:
    product = db.get(Product, product_id)
    raise_not_found_if_empty("product", product_id, product)
    return product


def get_products_by_category(*, db: Session, category_id: int, filter: Pagination) -> list[Product]:
    products = db.query(Product).join(Category).options(joinedload(Product.category)).filter(Product.category_id == category_id).offset(
        filter.offset).limit(filter.limit).all()
    raise_not_found_if_empty("category",
                             category_id, products, filter.offset)
    return products


def get_product_stat(*, db: Session, filter: ProductStatsMetric) -> int | float:
    metric = filter.metric

    if metric == "total_price":
        result = db.query(func.sum(Product.price)
                          ).scalar()
        return float(result) if result is not None else 0.0

    if metric == "max_price":
        result = db.query(func.max(Product.price)).scalar()
        return float(result) if result is not None else 0.0

    if metric == "min_price":
        result = db.query(func.min(Product.price)).scalar()
        return float(result) if result is not None else 0.0

    raise ValueError("Invalid metric specified")
