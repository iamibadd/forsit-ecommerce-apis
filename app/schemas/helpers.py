from pydantic import BaseModel, model_validator
from datetime import date


class Pagination(BaseModel):
    offset: int
    limit: int


class DateFilter(BaseModel):
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def check_dates(self) -> 'DateFilter':
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be greater than start_date")
        return self


class SortFilter(BaseModel):
    sort_order: str


class PaginatedDateFilter(Pagination, DateFilter):
    pass
