from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .products import Product
    from .inventory_history import InventoryHistory


class InventoryBase(SQLModel):
    quantity: int = Field(nullable=False)


class Inventory(InventoryBase, table=True):
    __tablename__ = 'inventory'

    id: int | None = Field(default=None, primary_key=True, index=True)
    product_id: int = Field(foreign_key="products.id", ondelete="CASCADE", index=True)

    # Relationships
    product: list["Product"] = Relationship(back_populates="inventory")
    history: list["InventoryHistory"] = Relationship(
        back_populates="inventory")
