from sqlalchemy import Column, Integer, ForeignKey
from app.database.base import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
