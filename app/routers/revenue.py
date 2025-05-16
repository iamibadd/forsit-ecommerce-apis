from fastapi import APIRouter, Query
from typing import Annotated

from app.dependencies import (
    SessionDep, PaginationDep, PaginatedDateFilterDep)
from app.crud import revenue as revenue_crud
from app.schemas.revenue import (
    Revenue, RevenueDatePeriod, RevenueComparisonFilter, RevenuePeriodResponse, RevenueComparisonResponse)


router = APIRouter(prefix="/revenue", tags=["Revenue"])


@router.get("", response_model=list[Revenue])
def get_revenue(
    db: SessionDep,
    filter: PaginationDep,
):
    revenue = revenue_crud.get_revenue(db=db, filter=filter)
    return revenue


@router.get("/by_date_range", response_model=list[Revenue])
def get_revenue_by_date_range(
    db: SessionDep,
    filter: PaginatedDateFilterDep,
):
    revenue = revenue_crud.get_revenue_by_date_range(db=db, filter=filter)
    return revenue


@router.get("/by_time_period",
            summary="Returns total revenue, top N sales, and bottom N sales for the given time period.",
            response_model=RevenuePeriodResponse)
def get_revenue_by_period(
    db: SessionDep,
    filter: Annotated[RevenueDatePeriod, Query(description="Filter by time period")],
    count: Annotated[int, Query(description="Get top and low sales")] = 5,
):
    revenue = revenue_crud.get_revenue_by_period(
        db=db, filter=filter, count=count)
    return revenue


@router.get("/by_time_period",
            summary="Get total revenue, top N sales, and bottom N sales for the given time period.",
            response_model=RevenuePeriodResponse)
def compare_revenue_by_category(
    db: SessionDep,
    filter: Annotated[RevenueDatePeriod, Query(description="Filter by time period")],
    count: Annotated[int, Query(description="Get top and low sales")] = 5,
):
    revenue = revenue_crud.compare_revenue_by_category(
        db=db, filter=filter, count=count)
    return revenue


@router.get("/compare", summary='Compare revenue between two dates', response_model=RevenueComparisonResponse)
def compare_revenue_periods(
    db: SessionDep,
    filter: Annotated[RevenueComparisonFilter, Query(description="Compare revenue by dates")],
):
    revenue = revenue_crud.compare_revenue_periods(db=db, filter=filter)
    return revenue
