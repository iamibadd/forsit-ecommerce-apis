from pydantic import BaseModel, model_validator
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


class RevenueDatePeriod(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    annual = "annual"


class RevenuePeriodResponse(BaseModel):
    total_revenue: float
    top_sales: list[Revenue]
    low_sales: list[Revenue]


class RevenueComparisonFilter(BaseModel):
    start_date_1: date
    end_date_1: date
    start_date_2: date
    end_date_2: date

    @model_validator(mode="after")
    def check_date_order(self) -> 'RevenueComparisonFilter':
        if self.start_date_1 <= self.start_date_2:
            raise ValueError("start_date_1 must be greater than start_date_2")
        if self.end_date_1 <= self.end_date_2:
            raise ValueError("end_date_1 must be greater than end_date_2")
        return self


class RevenuePeriodFields(BaseModel):
    start_date: date
    end_date: date
    total_revenue: float


class RevenueComparisonResponse(BaseModel):
    period_1: RevenuePeriodFields
    period_2: RevenuePeriodFields
    difference_in_revenue: float
