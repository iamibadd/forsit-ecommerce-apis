from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, func
from datetime import datetime, timezone

if TYPE_CHECKING:
    from .inventory import Inventory


class InventoryHistoryBase(SQLModel):
    changed_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    previous_quantity: int
    new_quantity: int
    description: str | None = Field(default='Manual updation')


class InventoryHistory(InventoryHistoryBase, table=True):
    __tablename__ = 'inventory_history'

    id: int | None = Field(default=None, primary_key=True)
    inventory_id: int = Field(foreign_key="inventory.id", ondelete="CASCADE", index=True)

    # Relationships
    inventory: list["Inventory"] = Relationship(back_populates="history")
