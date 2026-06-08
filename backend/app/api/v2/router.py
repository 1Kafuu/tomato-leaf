from fastapi import APIRouter
from .endpoints import prediction

api_router = APIRouter()
api_router.include_router(prediction.router, tags=["prediction"])