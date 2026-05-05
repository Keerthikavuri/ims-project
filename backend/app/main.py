import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import signals, incidents, health
from app.db.postgres import init_db
from app.db.mongo import close_mongo
from app.db.redis_client import close_redis
from app.services.worker import start_worker

app = FastAPI(
    title="Incident Management System",
    description="Mission-Critical IMS for distributed stack monitoring",
    version="1.0.0"
)

# CORS — React frontend connect 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(signals.router, tags=["Signals"])
app.include_router(incidents.router, tags=["Incidents"])
app.include_router(health.router, tags=["Health"])


@app.on_event("startup")
async def startup():
    print("[IMS] Starting up...")
    # PostgreSQL tables 
    await init_db()
    # Background worker start 
    asyncio.create_task(start_worker())
    print("[IMS] System ready!")


@app.on_event("shutdown")
async def shutdown():
    print("[IMS] Shutting down...")
    await close_mongo()
    await close_redis()
    print("[IMS] Shutdown complete.")