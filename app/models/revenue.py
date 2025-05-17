from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import date


if TYPE_CHECKING:
    from .sales import Sale


class RevenueBase(SQLModel):
    revenue_amount: float = Field(nullable=False)
    created_at: date


class Revenue(RevenueBase, table=True):
    __tablename__ = 'revenue'

    id: int | None = Field(default=None, primary_key=True, index=True)
    sale_id: int = Field(foreign_key="sales.id", ondelete="CASCADE", index=True)

    # Relationships
    sales: list["Sale"] = Relationship(back_populates="revenue")
