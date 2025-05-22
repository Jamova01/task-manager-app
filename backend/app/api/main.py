from fastapi import APIRouter

from app.api.routes import login, users, tasks


api_router = APIRouter()

api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(tasks.router)
