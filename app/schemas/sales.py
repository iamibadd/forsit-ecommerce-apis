from pydantic import BaseModel
from datetime import date
from enum import Enum

from .products import Product, ProductCategory


class SalesBase(BaseModel):
    product_id: int
    quantity: int
    total_price: float
    sale_date: date | None = None


class Sales(SalesBase):
    id: int | None

    class Config:
        from_attributes = True


class SalesProducts(Sales):
    product: Product

    class Config:
        from_attributes = True


class SalesProductCategory(Sales):
    product: ProductCategory

    class Config:
        from_attributes = True


class SalesMetric(str, Enum):
    total_sales = "total_sales"
    total_quantity = "total_quantity"
    total_amount = "total_amount"


class SalesStatsMetric(BaseModel):
    start_date: date | None = None
    end_date: date | None = None
    metric: SalesMetric
