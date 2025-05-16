from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Product, Revenue, Category
from app.schemas.helpers import Pagination, PaginatedDateFilter, DateFilter
from app.schemas.revenue import RevenuePeriod


def get_revenue(*, db: Session, filter: Pagination) -> list[Revenue]:
    return db.query(Revenue).offset(filter.offset).limit(filter.limit).all()


def get_revenue_by_date_range(*, db: Session, filter: PaginatedDateFilter) -> list[Revenue]:
    return db.query(Revenue).filter(Revenue.created_at.between(filter.start_date, filter.end_date)).offset(filter.offset).limit(filter.limit).all()


def get_revenue_by_period(db: Session, period: RevenuePeriod):
    if period == "daily":
        return db.query(Revenue).filter(func.date(Revenue.created_at) == func.current_date()).all()
    elif period == "weekly":
        return db.query(Revenue).filter(func.date(Revenue.created_at) >= func.date_sub(func.current_date(), func.interval(1, 'week'))).all()
    elif period == "monthly":
        return db.query(Revenue).filter(func.date(Revenue.created_at) >= func.date_sub(func.current_date(), func.interval(1, 'month'))).all()
    elif period == "annual":
        return db.query(Revenue).filter(func.date(Revenue.created_at) >= func.date_sub(func.current_date(), func.interval(1, 'year'))).all()


def compare_revenue(db: Session, filter: DateFilter):
    return db.query(Revenue).filter(
        Revenue.period.in_([filter.start_date, filter.end_date])
    ).all()


def compare_revenue_by_category(db: Session):
    return db.query(Revenue, Category.name).join(Product).join(Category).group_by(Category.id).all()
