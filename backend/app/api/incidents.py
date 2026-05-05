from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.postgres import get_db
from app.db.redis_client import get_redis
from app.db.mongo import get_signals_collection
from app.models.work_item import WorkItem, RCARecord
from app.schemas.signal import WorkItemOut, RCAIn, RCAOut
from app.services.state_machine import StateMachine
from datetime import datetime
import json

router = APIRouter()


# All incidents list
@router.get("/incidents", response_model=list[WorkItemOut])
async def get_incidents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(WorkItem).order_by(WorkItem.created_at.desc())
    )
    return result.scalars().all()


# Single incident detail
@router.get("/incidents/{incident_id}", response_model=WorkItemOut)
async def get_incident(incident_id: str, db: AsyncSession = Depends(get_db)):
    # Direct DB query 
    result = await db.execute(
        select(WorkItem).where(WorkItem.id == incident_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Incident not found")
    return item


# Incident signals — MongoDB 
@router.get("/incidents/{incident_id}/signals")
async def get_incident_signals(incident_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(WorkItem).where(WorkItem.id == incident_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Incident not found")

    collection = get_signals_collection()
    signals = await collection.find(
        {"component_id": item.component_id}
    ).to_list(length=100)

    for s in signals:
        s["_id"] = str(s["_id"])
    return signals


# Status transition
@router.patch("/incidents/{incident_id}/status")
async def update_status(
    incident_id: str,
    new_status: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(WorkItem).where(WorkItem.id == incident_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Incident not found")

    # CLOSED 
    if new_status == "CLOSED":
        rca_result = await db.execute(
            select(RCARecord).where(RCARecord.work_item_id == incident_id)
        )
        rca = rca_result.scalars().first()
        if not rca:
            raise HTTPException(
                status_code=400,
                detail="Cannot close incident without RCA. Submit RCA first."
            )

    # State machine transition
    sm = StateMachine(item.status)
    try:
        item.status = sm.transition(new_status)
        if new_status == "CLOSED":
            item.end_time = datetime.utcnow()
            if item.start_time:
                item.mttr_seconds = (
                    item.end_time - item.start_time
                ).total_seconds()
        await db.commit()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"status": item.status, "mttr_seconds": item.mttr_seconds}


# RCA Submit
@router.post("/incidents/{incident_id}/rca", response_model=RCAOut)
async def submit_rca(
    incident_id: str,
    rca_data: RCAIn,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(WorkItem).where(WorkItem.id == incident_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Incident not found")

    if item.status == "CLOSED":
        raise HTTPException(
            status_code=400,
            detail="Incident already closed."
        )

    rca = RCARecord(
        work_item_id=incident_id,
        incident_start=rca_data.incident_start,
        incident_end=rca_data.incident_end,
        root_cause_category=rca_data.root_cause_category,
        fix_applied=rca_data.fix_applied,
        prevention_steps=rca_data.prevention_steps,
    )
    db.add(rca)
    await db.commit()
    await db.refresh(rca)
    return rca