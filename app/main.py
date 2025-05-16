from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.session import create_db_and_tables
from app.routers import users, auth, products, sales


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="Forsit E-commerce Admin API", lifespan=lifespan)


app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(sales.router, prefix="/api/sales", tags=["Sales"])


@app.get("/", tags=['Health Check'])
def health_check():
    return {"Server is": "Healthy!!"}
