from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import users as user_model
from app.models import products as products_model
from app.models import sales as sales_model
from app.models import revenue as revenue_model
from app.models import inventory as inventory_model
from app.config import settings


SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       pool_size=20,
                       max_overflow=10,
                       pool_timeout=30,
                       pool_recycle=1800,
                       pool_pre_ping=True
                       )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
user_model.Base.metadata.create_all(bind=engine)
products_model.Base.metadata.create_all(bind=engine)
sales_model.Base.metadata.create_all(bind=engine)
revenue_model.Base.metadata.create_all(bind=engine)
inventory_model.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
