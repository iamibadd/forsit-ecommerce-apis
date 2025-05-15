from sqlalchemy import Column, Integer, DECIMAL, DateTime, ForeignKey
from app.database.base import Base


class Revenue(Base):
    __tablename__ = "revenue"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey('sales.id'))
    revenue_amount = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, nullable=False)
