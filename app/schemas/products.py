from pydantic import BaseModel
from enum import Enum
from .category import Category


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    category_id: int
    price: float


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True


class ProductCategory(Product):
    category: Category

    class Config:
        from_attributes = True


class ProductMetric(str, Enum):
    total_price = "total_price"
    max_price = "max_price"
    min_price = "min_price"


class ProductStatsMetric(BaseModel):
    metric: ProductMetric
