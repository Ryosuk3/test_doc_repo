from contextlib import asynccontextmanager
from datetime import UTC, datetime

from fastapi import FastAPI

from app.routers import items


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.started_at = datetime.now(UTC)
    yield


app = FastAPI(
    title="Test FastAPI Service",
    description="A small service intended for experiments and modifications.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(items.router)


@app.get("/", tags=["system"])
async def root() -> dict[str, str]:
    return {"message": "Test FastAPI service is running"}


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
