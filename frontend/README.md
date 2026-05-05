# Incident Management System (IMS)
## Zeotap Infrastructure / SRE Intern Assignment

A mission-critical Incident Management System that detects infrastructure failures, creates work items, tracks resolution workflow, and enforces Root Cause Analysis before closing incidents.

## Architecture
- **Signal Generator** → Mock script simulating infrastructure failures
- **Ingestion API** → FastAPI with Rate Limiter (500 req/sec)
- **Async Queue** → In-memory buffer handling 10k signals/sec
- **Consumer Worker** → Debounce logic, Strategy Pattern, State Machine
- **MongoDB** → Raw signals storage (audit log)
- **PostgreSQL** → Work Items, RCA records (source of truth)
- **Redis** → Hot path cache for dashboard
- **React Dashboard** → Live feed, Incident details, RCA form

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Backend | Python FastAPI |
| Queue | asyncio.Queue |
| NoSQL | MongoDB |
| RDBMS | PostgreSQL |
| Cache | Redis |
| Frontend | React |
| Deploy | Docker Compose |

## Design Patterns
- **Strategy Pattern** → Alert priority (P0/P1/P2) based on component type
- **State Pattern** → Work Item lifecycle: OPEN → INVESTIGATING → RESOLVED → CLOSED

## How to Run
### Prerequisites
- Docker Desktop
- Git

### Steps
```bash
git clone https://github.com/Keerthikavuri/ims-project.git
cd ims-project
docker-compose up --build
```

### Access
- Dashboard: http://localhost:3000
- API: http://localhost:8000
- Health: http://localhost:8000/health

### Generate Mock Signals
```bash
cd ims-project
pip install httpx
python mock_signals.py
```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /signals | Ingest infrastructure signal |
| GET | /incidents | List all incidents |
| GET | /incidents/{id} | Get incident details |
| PATCH | /incidents/{id}/status | Update incident status |
| POST | /incidents/{id}/rca | Submit RCA |
| GET | /health | System health check |

## Security & Performance
- Rate limiting: 500 requests/second
- Debounce: 100 signals/10 seconds = 1 Work Item
- Redis caching for dashboard hot path
- Retry logic for database writes
- CORS enabled for frontend access

## GitHub
https://github.com/Keerthikavuri/ims-project