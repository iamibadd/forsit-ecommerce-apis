from fastapi import FastAPI
from app.routers import users, auth, products, sales


app = FastAPI(title="Forsit E-commerce Admin API")

app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(sales.router, prefix="/api/sales", tags=["Sales"])


@app.get("/", tags=['Health Check'])
def health_check():
    return {"Server is": "Healthy!!"}
