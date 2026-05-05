# Incident Management System (IMS)
## Zeotap Infrastructure / SRE Intern Assignment

A mission-critical Incident Management System that detects infrastructure failures, creates work items, tracks resolution workflow, and enforces Root Cause Analysis before closing incidents.

---

## Architecture Diagram

```
Signal Generator (mock_signals.py)
         |
         v
+------------------+
|  Ingestion API   |  POST /signals
|  Rate Limiter    |  500 req/sec max
+------------------+
         |
         v
+------------------+
|  Async Queue     |  asyncio.Queue
|  (Backpressure)  |  Max 50,000 signals
+------------------+
         |
         v
+--------------------------------+
|      Consumer Worker           |
|  - Debounce (100 signals/10s)  |
|  - Strategy Pattern (P0/P1/P2) |
|  - State Machine               |
|  - Retry Logic (3 attempts)    |
+--------------------------------+
         |              |
         v              v
+------------+   +---------------+
|  MongoDB   |   |  PostgreSQL   |
| Raw Signals|   | Work Items    |
| Audit Log  |   | RCA Records   |
+------------+   +---------------+
         |              |
         +--------------+
                |
                v
        +-------------+
        | Redis Cache |
        | Hot Path    |
        +-------------+
                |
                v
        +--------------+
        | Backend API  |
        | /incidents   |
        | /rca /health |
        +--------------+
                |
                v
        +----------------+
        | React Dashboard|
        | Live Feed      |
        | RCA Form       |
        +----------------+
```

---

## Data Flow Explanation

1. **Signal Generator** sends JSON payloads (component failures) to `POST /signals`
2. **Ingestion API** rate limits to 500 req/sec — excess requests return 429
3. **Async Queue** buffers up to 50,000 signals — if full, signals are dropped gracefully (backpressure)
4. **Consumer Worker** reads from queue:
   - **Debounce**: 100+ signals for same component in 10 seconds = only 1 Work Item created
   - **Strategy Pattern**: RDBMS/MCP = P0, API/QUEUE = P1, CACHE/NOSQL = P2
   - **State Machine**: enforces OPEN → INVESTIGATING → RESOLVED → CLOSED
5. Raw signals saved to **MongoDB** (audit log, flexible schema)
6. Work Items + RCA saved to **PostgreSQL** (source of truth, ACID)
7. Active incidents cached in **Redis** (fast dashboard load, 300s TTL)

---

## Backpressure Handling

When signal volume exceeds queue capacity (50,000):
- New signals are **dropped gracefully** (system does not crash)
- Warning logged: `[WARN] Queue full! Dropping signal`
- System remains stable under 10,000+ signals/sec bursts
- Metrics printed every 5 seconds showing throughput and total processed

---

## MTTR & RCA Enforcement

- **MTTR** (Mean Time To Resolve) = `end_time - start_time` in seconds
- Automatically calculated when incident moves to CLOSED
- **RCA is mandatory** — incident cannot be CLOSED without submitting:
  - Root Cause Category (INFRA / CODE / CONFIG / NETWORK / HUMAN)
  - Fix Applied
  - Prevention Steps

---

## Folder Structure

```
ims-project/
├── docker-compose.yml        # Orchestrates all 5 services
├── mock_signals.py           # Signal generator script
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py           # FastAPI app entry point
│       ├── api/
│       │   ├── signals.py    # POST /signals + rate limiter
│       │   ├── incidents.py  # Incidents + RCA endpoints
│       │   └── health.py     # /health endpoint
│       ├── core/
│       │   └── config.py     # Settings
│       ├── db/
│       │   ├── mongo.py      # MongoDB connection
│       │   ├── postgres.py   # PostgreSQL connection
│       │   └── redis_client.py # Redis connection
│       ├── models/
│       │   └── work_item.py  # SQLAlchemy models
│       ├── schemas/
│       │   └── signal.py     # Pydantic schemas
│       └── services/
│           ├── worker.py         # Consumer worker + metrics
│           ├── queue_service.py  # Async queue
│           ├── alert_strategy.py # Strategy pattern
│           └── state_machine.py  # State pattern
└── frontend/
    ├── Dockerfile
    ├── nginx.conf
    └── src/
        ├── App.js
        ├── api/client.js
        ├── pages/
        │   ├── Dashboard.js
        │   └── IncidentDetail.js
        └── components/
            ├── IncidentCard.js
            ├── RCAForm.js
            └── StatusBadge.js
```

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Backend | Python FastAPI | Async, high performance |
| Queue | asyncio.Queue | In-memory, no extra service |
| NoSQL | MongoDB | Flexible schema, fast writes |
| RDBMS | PostgreSQL | ACID transactions, structured data |
| Cache | Redis | Sub-millisecond reads |
| Frontend | React | Component-based, live updates |
| Deploy | Docker Compose | One command setup |

---

## Design Patterns

- **Strategy Pattern** → Alert priority (P0/P1/P2) based on component type
- **State Pattern** → Work Item lifecycle: OPEN → INVESTIGATING → RESOLVED → CLOSED

---

## Security & Performance (Bonus Points)

- Rate limiting: 500 requests/second (returns 429 on exceed)
- Debounce: 100 signals/10 seconds = 1 Work Item (prevents noise)
- Redis caching for dashboard hot path (300s TTL)
- Retry logic (3 attempts) for database writes
- CORS enabled for frontend access
- Backpressure: queue overflow protection (graceful drop)

---

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
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Generate Mock Signals

```bash
pip install httpx
python mock_signals.py
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /signals | Ingest infrastructure signal |
| GET | /incidents | List all incidents |
| GET | /incidents/{id} | Get incident details |
| PATCH | /incidents/{id}/status | Update incident status |
| POST | /incidents/{id}/rca | Submit RCA |
| GET | /health | System health check |

---

## RCA Guide

When closing an incident, fill the RCA form:

| Field | Example |
|-------|---------|
| Root Cause Category | INFRA |
| Fix Applied | Restarted service and cleared memory leak |
| Prevention Steps | Added monitoring alerts at 80% threshold |

> Note: RCA must be submitted before moving incident to CLOSED. MTTR is auto-calculated on closure.

---

## GitHub
https://github.com/Keerthikavuri/ims-project