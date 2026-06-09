from fastapi import APIRouter
from .endpoints import prediction, history

api_router = APIRouter()
api_router.include_router(prediction.router, tags=["prediction"])
api_router.include_router(history.router, prefix="/history", tags=["history"])
