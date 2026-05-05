import asyncio
from app.core.config import settings

# Single global in-memory queue — backpressure buffer
_signal_queue: asyncio.Queue | None = None


def get_signal_queue() -> asyncio.Queue:
    global _signal_queue
    if _signal_queue is None:
        _signal_queue = asyncio.Queue(maxsize=settings.queue_max_size)
    return _signal_queue


async def enqueue_signal(signal: dict) -> bool:
    queue = get_signal_queue()
    try:
        # nowait 
        queue.put_nowait(signal)
        return True
    except asyncio.QueueFull:
        print(f"[WARN] Queue full! Dropping signal for {signal.get('component_id')}")
        return False


def get_queue_size() -> int:
    queue = get_signal_queue()
    return queue.qsize()