import os
import sys
import logging
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure project root is importable (for ../blockchain)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from config import settings  # noqa: E402
from database import init_db  # noqa: E402
from api.router import api_router  # noqa: E402

# Logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("green-food-api")

app = FastAPI(
    title="绿色食品交易平台接口",
    description="面向绿色食品交易与区块链溯源的后端接口（示例实现）",
    version=settings.VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    # Create tables
    init_db()
    logger.info("✅ Database initialized")


@app.get("/health", tags=["系统"])
def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "service": settings.APP_NAME,
        "version": settings.VERSION,
    }


@app.get("/", tags=["系统"])
def root():
    return {"message": "绿色食品交易平台接口", "docs": "/docs", "health": "/health"}


app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
