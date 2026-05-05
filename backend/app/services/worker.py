import asyncio
import time
from datetime import datetime
from app.services.queue_service import get_signal_queue
from app.services.alert_strategy import get_alert_strategy
from app.db.mongo import get_signals_collection
from app.db.postgres import AsyncSessionLocal
from app.db.redis_client import get_redis
from app.models.work_item import WorkItem
from sqlalchemy import select
import json

# Debounce tracker — component_id: last_window_start
_debounce_tracker: dict[str, dict] = {}

# Metrics
_processed_count = 0
_last_metrics_time = time.time()


async def process_signal(signal: dict):
    global _processed_count
    component_id = signal["component_id"]
    component_type = signal["component_type"]
    now = datetime.utcnow()

    # 1. Save raw signal to MongoDB
    try:
        collection = get_signals_collection()
        await collection.insert_one({**signal, "received_at": now.isoformat()})
    except Exception as e:
        print(f"[ERROR] MongoDB write failed: {e}")

    # 2. Debounce logic — 100 signals / 10 seconds = 1 work item
    tracker = _debounce_tracker.get(component_id)
    if tracker:
        tracker["count"] += 1
        elapsed = (now - tracker["window_start"]).total_seconds()
        from app.core.config import settings
        if elapsed <= settings.debounce_window_seconds:
            if tracker["count"] <= settings.debounce_threshold:
                return  # Skip — already have work item
        else:
            # Reset window
            _debounce_tracker[component_id] = {
                "window_start": now,
                "count": 1
            }
    else:
        _debounce_tracker[component_id] = {
            "window_start": now,
            "count": 1
        }

    # 3. Get alert strategy
    strategy = get_alert_strategy(component_type)
    priority = strategy.get_priority()
    message = strategy.get_message(component_id)
    print(f"[ALERT] {message}")

    # 4. Create Work Item in PostgreSQL (with retry)
    for attempt in range(3):
        try:
            async with AsyncSessionLocal() as session:
                # Check if open work item exists
                result = await session.execute(
                    select(WorkItem).where(
                        WorkItem.component_id == component_id,
                        WorkItem.status != "CLOSED"
                    )
                )
                existing = result.scalar_one_or_none()
                if existing:
                    existing.signal_count += 1
                    await session.commit()
                else:
                    work_item = WorkItem(
                        component_id=component_id,
                        priority=priority,
                        status="OPEN",
                        start_time=now,
                    )
                    session.add(work_item)
                    await session.commit()

                    # 5. Update Redis cache
                    redis = await get_redis()
                    await redis.setex(
                        f"incident:{work_item.id}",
                        300,
                        json.dumps({
                            "id": work_item.id,
                            "component_id": component_id,
                            "priority": priority,
                            "status": "OPEN",
                        })
                    )
            break
        except Exception as e:
            print(f"[ERROR] Postgres write attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(0.5)

    _processed_count += 1


async def metrics_printer():
    global _processed_count, _last_metrics_time
    while True:
        await asyncio.sleep(5)
        now = time.time()
        elapsed = now - _last_metrics_time
        rate = _processed_count / elapsed if elapsed > 0 else 0
        print(f"[METRICS] Throughput: {rate:.1f} signals/sec | Total: {_processed_count}")
        _processed_count = 0
        _last_metrics_time = now


async def start_worker():
    queue = get_signal_queue()
    print("[WORKER] Consumer worker started...")
    asyncio.create_task(metrics_printer())
    while True:
        signal = await queue.get()
        asyncio.create_task(process_signal(signal))
        queue.task_done()