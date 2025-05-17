from pydantic import BaseModel


class InventoryBase(BaseModel):
    product_id: int


class InventoryUpdate(BaseModel):
    description: str | None = None
    new_quantity: int


class Inventory(InventoryBase):
    id: int
    quantity: int

    class Config:
        from_attributes = True
