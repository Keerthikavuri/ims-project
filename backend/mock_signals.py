import httpx
import asyncio
import random
from datetime import datetime

BASE_URL = "http://localhost:8000"

COMPONENTS = [
    {"component_id": "RDBMS_PRIMARY_01", "component_type": "RDBMS"},
    {"component_id": "CACHE_CLUSTER_01", "component_type": "CACHE"},
    {"component_id": "API_GATEWAY_01", "component_type": "API"},
    {"component_id": "QUEUE_BROKER_01", "component_type": "QUEUE"},
    {"component_id": "NOSQL_STORE_01", "component_type": "NOSQL"},
    {"component_id": "MCP_HOST_01", "component_type": "MCP"},
]

ERROR_TYPES = [
    "CONNECTION_TIMEOUT",
    "HIGH_LATENCY",
    "MEMORY_OVERFLOW",
    "DISK_FULL",
    "SERVICE_UNAVAILABLE",
]


async def send_signal(client: httpx.AsyncClient, component: dict):
    payload = {
        "component_id": component["component_id"],
        "component_type": component["component_type"],
        "error_type": random.choice(ERROR_TYPES),
        "message": f"{component['component_id']} failure detected!",
        "timestamp": datetime.utcnow().isoformat(),
    }
    try:
        response = await client.post(f"{BASE_URL}/signals", json=payload)
        print(f"[SENT] {payload['component_id']} → {response.status_code}")
    except Exception as e:
        print(f"[ERROR] {e}")


async def simulate_rdbms_outage():
    print("\n[SIM] Simulating RDBMS outage — 100 signals in 10 seconds...")
    async with httpx.AsyncClient() as client:
        tasks = []
        for _ in range(100):
            tasks.append(send_signal(client, COMPONENTS[0]))
        await asyncio.gather(*tasks)


async def simulate_random_failures():
    print("\n[SIM] Simulating random failures across stack...")
    async with httpx.AsyncClient() as client:
        for _ in range(20):
            component = random.choice(COMPONENTS)
            await send_signal(client, component)
            await asyncio.sleep(0.2)


async def main():
    print("=" * 50)
    print("  IMS Mock Signal Generator")
    print("=" * 50)

    # RDBMS outage simulate 
    await simulate_rdbms_outage()
    await asyncio.sleep(2)

    # Random failures simulate 
    await simulate_random_failures()

    print("\n[DONE] Mock signals sent!")


if __name__ == "__main__":
    asyncio.run(main())