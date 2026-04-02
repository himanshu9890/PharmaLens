import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.trials import router as trials_router
from backend.cache.redis_client import close_redis
from backend.config import settings
from backend.db.database import create_tables

logging.basicConfig(level=logging.INFO if not settings.debug else logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PharmaLens API",
    description="AI-powered pharma BD intelligence platform",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.cors_allow_all else settings.cors_origins,
    allow_credentials=not settings.cors_allow_all,  # credentials incompatible with wildcard
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trials_router, prefix=settings.api_v1_prefix)


@app.on_event("startup")
async def startup() -> None:
    logger.info("Starting PharmaLens API...")
    await create_tables()
    logger.info("Database tables ready.")


@app.on_event("shutdown")
async def shutdown() -> None:
    await close_redis()


@app.get("/api/v1/health", tags=["meta"])
async def health() -> dict:
    return {"status": "ok", "version": "0.1.0"}
