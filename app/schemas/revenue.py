from pydantic import BaseModel
from datetime import date
from enum import Enum

from .sales import Sales


class RevenueBase(BaseModel):
    sale_id: int
    revenue_amount: float
    created_at: date


class Revenue(RevenueBase):
    id: int | None

    class Config:
        from_attributes = True


class RevenueSales(Revenue):
    sales: Sales

    class Config:
        from_attributes = True


class RevenuePeriod(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    annual = "annual"
