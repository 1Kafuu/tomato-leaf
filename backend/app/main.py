from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine
from app.models.base import Base
from app.api.v1.router import api_router as api_router_v1
from app.api.v2.router import api_router as api_router_v2

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    if engine is not None:
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        except Exception as e:
            print(f"Warning: Could not initialize database: {e}")
    yield
    # Cleanup on shutdown
    if engine is not None:
        try:
            await engine.dispose()
        except Exception as e:
            print(f"Warning: Could not dispose database: {e}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Should be restricted in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router_v1, prefix=settings.API_V1_STR)
app.include_router(api_router_v2, prefix="/api/v2")

@app.get("/")
def root():
    return {"message": "Welcome to Tomato Leaf Health Detection API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
