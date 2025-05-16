from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from app.database.session import create_db_and_tables
from app.routers import users, auth, products, sales


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="Forsit E-commerce Admin API", lifespan=lifespan)

api_v2_router = APIRouter(prefix="/v2/api")
api_v2_router.include_router(users.router)
api_v2_router.include_router(auth.router)
api_v2_router.include_router(products.router)
api_v2_router.include_router(sales.router)

app.include_router(api_v2_router)


@app.get("/", tags=['Health Check'])
def health_check():
    return {"Server is": "Healthy!!"}
