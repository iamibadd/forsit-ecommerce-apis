from sqlalchemy import Column, Integer, DECIMAL, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    sale_date = Column(Date, nullable=False)

    product = relationship("Product", back_populates="sales")
