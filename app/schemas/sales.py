from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .products import Product, ProductCategory


class SalesBase(BaseModel):
    product_id: int
    quantity: int
    total_price: float
    sale_date: Optional[datetime] = None


class Sales(SalesBase):
    id: int

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
