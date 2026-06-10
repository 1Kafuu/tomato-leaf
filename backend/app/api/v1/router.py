from fastapi import APIRouter

from .endpoints import auth, prediction, history

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(prediction.router, tags=["prediction"])
api_router.include_router(history.router, prefix="/history", tags=["history"])
