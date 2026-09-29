from fastapi import APIRouter
from src.adapters.inbound.rest import health

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
