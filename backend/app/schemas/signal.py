from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class SignalIn(BaseModel):
    component_id: str
    component_type: str
    error_type: str
    message: str
    timestamp: Optional[datetime] = None


class WorkItemOut(BaseModel):
    id: str
    component_id: str
    priority: str
    status: str
    signal_count: int
    start_time: datetime
    end_time: Optional[datetime] = None
    mttr_seconds: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


class RCAIn(BaseModel):
    work_item_id: str
    incident_start: datetime
    incident_end: datetime
    root_cause_category: str
    fix_applied: str
    prevention_steps: str

    @field_validator('incident_start', 'incident_end', mode='before')
    @classmethod
    def parse_datetime(cls, v):
        if isinstance(v, str):
            for fmt in [
                '%Y-%m-%dT%H:%M',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%dT%H:%M:%S.%f',
            ]:
                try:
                    return datetime.strptime(v, fmt)
                except ValueError:
                    continue
        return v


class RCAOut(BaseModel):
    id: str
    work_item_id: str
    incident_start: datetime
    incident_end: datetime
    root_cause_category: str
    fix_applied: str
    prevention_steps: str
    submitted_at: datetime

    class Config:
        from_attributes = True