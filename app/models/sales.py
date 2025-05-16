from typing import TYPE_CHECKING
from datetime import date
from sqlmodel import SQLModel, Field, Relationship, Date

if TYPE_CHECKING:
    from .products import Product
    from .revenue import Revenue


class SaleBase(SQLModel):
    quantity: int
    total_price: float
    sale_date: date


class Sale(SaleBase, table=True):
    __tablename__ = "sales"

    id: int | None = Field(default=None, primary_key=True, index=True)
    product_id: int = Field(foreign_key="products.id", ondelete="CASCADE")

    # Relationships
    product: list["Product"] = Relationship(back_populates="sales")
    revenue: list["Revenue"] = Relationship(back_populates="sales")
