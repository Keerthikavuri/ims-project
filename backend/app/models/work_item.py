import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Float, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.postgres import Base


class WorkItem(Base):
    __tablename__ = "work_items"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    component_id: Mapped[str] = mapped_column(String, nullable=False)
    priority: Mapped[str] = mapped_column(String, default="P2")
    status: Mapped[str] = mapped_column(String, default="OPEN")
    signal_count: Mapped[int] = mapped_column(default=1)
    start_time: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    mttr_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )


class RCARecord(Base):
    __tablename__ = "rca_records"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    work_item_id: Mapped[str] = mapped_column(String, nullable=False)
    incident_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    incident_end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    root_cause_category: Mapped[str] = mapped_column(String, nullable=False)
    fix_applied: Mapped[str] = mapped_column(Text, nullable=False)
    prevention_steps: Mapped[str] = mapped_column(Text, nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )