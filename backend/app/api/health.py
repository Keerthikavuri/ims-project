from fastapi import APIRouter
from app.db.redis_client import get_redis
from app.db.mongo import get_mongo_client
from app.services.queue_service import get_queue_size
import time

router = APIRouter()

_start_time = time.time()


@router.get("/health")
async def health_check():
    status = {
        "status": "ok",
        "uptime_seconds": round(time.time() - _start_time, 2),
        "queue_size": get_queue_size(),
        "services": {}
    }

    # Redis check
    try:
        redis = await get_redis()
        await redis.ping()
        status["services"]["redis"] = "ok"
    except Exception:
        status["services"]["redis"] = "down"
        status["status"] = "degraded"

    # MongoDB check
    try:
        client = get_mongo_client()
        await client.admin.command("ping")
        status["services"]["mongodb"] = "ok"
    except Exception:
        status["services"]["mongodb"] = "down"
        status["status"] = "degraded"

    return status