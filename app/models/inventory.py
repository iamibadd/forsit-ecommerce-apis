from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .products import Product


class InventoryBase(SQLModel):
    quantity: int = Field(nullable=False)


class Inventory(InventoryBase, table=True):
    __tablename__ = 'inventory'

    id: int | None = Field(default=None, primary_key=True, index=True)
    product_id: int = Field(foreign_key="products.id", ondelete="CASCADE")

    # Relationships
    product: list["Product"] = Relationship(back_populates="inventory")
