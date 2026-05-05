from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

_client: AsyncIOMotorClient | None = None


def get_mongo_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.mongo_uri)
    return _client


def get_signals_collection():
    client = get_mongo_client()
    return client.get_default_database()["raw_signals"]


async def close_mongo():
    global _client
    if _client:
        _client.close()
        _client = None