from pydantic import BaseModel
from datetime import datetime


class InventoryHistoryBase(BaseModel):
    inventory_id: int
    changed_at: datetime | None = None
    previous_quantity: int
    new_quantity: int
    description: str | None = None


class InventoryHistoryCreate(InventoryHistoryBase):
    pass


class InventoryHistoryUpdate(InventoryHistoryBase):
    pass


class InventoryHistory(InventoryHistoryBase):
    id: int

    class Config:
        from_attributes = True
