from typing import TYPE_CHECKING
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DECIMAL

if TYPE_CHECKING:
    from .category import Category
    from .sales import Sale
    from .inventory import Inventory


class ProductBase(SQLModel):
    name: str = Field(max_length=255)
    price: Decimal = Field(
        sa_column=Column(DECIMAL(10, 2), nullable=False),
        default=Decimal("0.00"),
    )
    description: str | None = None


class Product(ProductBase, table=True):
    __tablename__ = 'products'

    id: int | None = Field(default=None, primary_key=True, index=True)
    category_id: int = Field(foreign_key="categories.id",
                             nullable=False, ondelete="CASCADE", index=True)

    # Relationships
    category: list["Category"] = Relationship(back_populates="product")
    sales: list["Sale"] = Relationship(back_populates="product")
    inventory: list["Inventory"] = Relationship(back_populates="product")
