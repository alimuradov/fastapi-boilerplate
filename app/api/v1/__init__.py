from fastapi import APIRouter

from app.api.v1 import products
from app.api.v1 import users
from app.api.v1 import login
from app.api.v1 import notifications

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(products.router, prefix="/products", tags=["Товары"])
api_router.include_router(users.router, prefix="/users", tags=["Пользователи"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Уведомления"])