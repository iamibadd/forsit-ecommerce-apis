from pydantic import BaseModel
from datetime import date


class Pagination(BaseModel):
    offset: int
    limit: int


class DateFilter(BaseModel):
    start_date: date
    end_date: date


class SortFilter(BaseModel):
    sort_order: str


class PaginatedDateFilter(Pagination, DateFilter):
    pass
