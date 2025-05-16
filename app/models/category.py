from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .products import Product


class CategoryBase(SQLModel):
    name: str


class Category(CategoryBase, table=True):
    __tablename__ = "categories"

    id: int | None = Field(default=None, primary_key=True, index=True)

    # Relationships
    product: list["Product"] = Relationship(back_populates="category")
