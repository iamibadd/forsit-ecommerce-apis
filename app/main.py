from fastapi import FastAPI
from app.routers import users as user_routes
from app.routers import auth as auth_routes


app = FastAPI(title="Forsit E-commerce Admin API")

app.include_router(user_routes.router, prefix="/api/users", tags=["Users"])
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Auth"])

@app.get("/", tags=['Health Check'])
def health_check():
    return {"Server is": "Healthy!!"}