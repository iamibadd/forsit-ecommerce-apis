from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .category import Category


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int
    price: float


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True


class ProductCategory(Product):
    category: Category

    class Config:
        from_attributes = True
