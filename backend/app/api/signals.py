import time
from fastapi import APIRouter, HTTPException
from app.schemas.signal import SignalIn
from app.services.queue_service import enqueue_signal, get_queue_size
from app.core.config import settings

router = APIRouter()

# Rate limiter — simple token bucket
_request_times: list[float] = []


def is_rate_limited() -> bool:
    now = time.time()
    global _request_times
    # Last 1 second lo requests filter cheyyi
    _request_times = [t for t in _request_times if now - t < 1.0]
    if len(_request_times) >= settings.rate_limit_per_second:
        return True
    _request_times.append(now)
    return False


@router.post("/signals", status_code=202)
async def ingest_signal(signal: SignalIn):
    # Rate limit check
    if is_rate_limited():
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again shortly."
        )

    # Queue lo add cheyyi
    payload = signal.model_dump()
    success = await enqueue_signal(payload)

    if not success:
        raise HTTPException(
            status_code=503,
            detail="System overloaded. Signal dropped."
        )

    return {
        "status": "accepted",
        "queue_size": get_queue_size()
    }