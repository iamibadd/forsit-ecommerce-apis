from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timezone, timedelta

from app.models import Product, Revenue, Sale
from app.schemas.helpers import Pagination, PaginatedDateFilter
from app.schemas.revenue import (
    RevenueDatePeriod, RevenueComparisonFilter, RevenuePeriodResponse, RevenueComparisonResponse)


def get_revenue(*, db: Session, filter: Pagination) -> list[Revenue]:
    return db.query(Revenue).offset(filter.offset).limit(filter.limit).all()


def get_revenue_by_date_range(*, db: Session, filter: PaginatedDateFilter) -> list[Revenue]:
    return db.query(Revenue).filter(Revenue.created_at.between(filter.start_date, filter.end_date)).offset(filter.offset).limit(filter.limit).all()


def get_revenue_by_period(*, db: Session, filter: RevenueDatePeriod, count: int = 5) -> RevenuePeriodResponse:
    now = datetime.now(timezone.utc)

    match filter:
        case "daily":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        case "weekly":
            start_date = now - timedelta(weeks=1)
        case "monthly":
            start_date = now - timedelta(days=30)
        case "annual":
            start_date = now - timedelta(days=365)
        case _:
            raise ValueError("Invalid period")

    total_revenue = (
        db.query(func.sum(Revenue.revenue_amount))
        .filter(Revenue.created_at >= start_date)
        .scalar()
    ) or 0.0

    top_sales = (
        db.query(Revenue)
        .filter(Revenue.created_at >= start_date)
        .order_by(desc(Revenue.revenue_amount))
        .limit(count)
        .all()
    )

    low_sales = (
        db.query(Revenue)
        .filter(Revenue.created_at >= start_date)
        .order_by(Revenue.revenue_amount)
        .limit(count)
        .all()
    )

    result = RevenuePeriodResponse(total_revenue=total_revenue,
                                   top_sales=top_sales, low_sales=low_sales)
    return result


def compare_revenue_periods(*, db: Session, filter: RevenueComparisonFilter) -> RevenueComparisonResponse:
    revenue_1 = db.query(func.sum(Revenue.revenue_amount)) \
        .filter(Revenue.created_at.between(filter.start_date_1, filter.end_date_1)) \
        .scalar() or 0.0

    revenue_2 = db.query(func.sum(Revenue.revenue_amount)) \
        .filter(Revenue.created_at.between(filter.start_date_2, filter.end_date_2)) \
        .scalar() or 0.0

    result = RevenueComparisonResponse(
        period_1={
            "start_date": filter.start_date_1,
            "end_date": filter.end_date_1,
            "total_revenue": float(revenue_1),
        },
        period_2={
            "start_date": filter.start_date_2,
            "end_date": filter.end_date_2,
            "total_revenue": float(revenue_2),
        },
        difference_in_revenue=float(revenue_2 - revenue_1),
    )
    return result
