from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    description = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship("Category", back_populates="products")
    sales = relationship("Sale", back_populates="product")
