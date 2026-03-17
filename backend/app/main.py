from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import parking


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    yield


app = FastAPI(
    title="Taichung Parking Dashboard",
    description="台中市停車場即時車位查詢 API — 路外停車場 / 路邊停車路段",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(parking.router, prefix="/api/v1")


@app.get("/health", tags=["infra"])
async def health_check() -> dict[str, str]:
    return {"status": "ok", "env": settings.app_env}
