from sqlmodel import SQLModel, create_engine, Session
from app.config import settings


SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True
)


def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)


def get_db():
    with Session(engine) as session:
        yield session
