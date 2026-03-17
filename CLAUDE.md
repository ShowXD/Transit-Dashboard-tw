# Taichung Parking Dashboard — Development Guide

## Project Overview

Real-time parking availability dashboard for Taichung City.
Backend: FastAPI + PostgreSQL + Celery/Redis
Frontend: Vue 3 + Leaflet.js (map with availability markers)
Data: TDX API (off-street lots, on-street road sections)

## Branch Conventions

| Branch | Purpose |
|--------|---------|
| `main` | Production-ready code only |
| `develop` | Integration branch |
| `feat/db-schema` | Alembic migrations, model changes |
| `feat/tdx-fetcher` | TDX API client + Celery tasks |
| `feat/celery-scheduler` | Beat schedule tuning |
| `feat/api-routes` | FastAPI endpoint implementation |
| `feat/frontend-dashboard` | Vue components, Leaflet map |

## Local Development

```bash
# 1. Copy env file
cp backend/.env.example backend/.env

# 2. Start all services
docker compose up -d

# 3. Run DB migrations (first time)
docker compose exec api alembic upgrade head

# 4. Seed master data (Phase 2+)
docker compose exec celery celery -A app.workers.celery_app call app.workers.tasks.sync_parking_master_data

# 5. Frontend (separate terminal)
cd frontend && npm install && npm run dev
```

API docs: http://localhost:8000/docs

## Code Conventions

- Python 3.12+, type hints everywhere
- Immutable patterns: never mutate objects in-place
- Async all the way: `async def` for all I/O-bound operations
- UPSERT for TDX data: `INSERT ... ON CONFLICT DO UPDATE`
- Files <400 lines; split by domain

### Comments & Docstrings
- Only comment what isn't obvious from the code
- No docstrings that just restate the class/function name
- Task docstrings: list the TDX endpoint(s) used, nothing else
- No `# startup: add X here` placeholder comments — just leave it empty

### SQLAlchemy Models
- `Mapped[T]` (non-Optional) is already NOT NULL — never add `nullable=False`
- `Mapped[int | None]` infers `Integer`; `Mapped[float | None]` infers `Float` — omit from `mapped_column()`
- Always keep `String(N)` — length constraints are enforced at the DB level
- Use `IntEnum` / `StrEnum` for typed constants instead of inline comments
- Example:
  ```python
  # WRONG
  name: Mapped[str] = mapped_column(String(128), nullable=False)
  car_park_type: Mapped[int | None] = mapped_column(Integer)

  # CORRECT
  name: Mapped[str] = mapped_column(String(128))
  car_park_type: Mapped[int | None] = mapped_column()
  ```

## DB Rules

- All tables: `created_at` / `updated_at` via `TimestampMixin`
- FKs use `ondelete="CASCADE"`
- Unique constraints define upsert keys

## Celery Task Rules

- Tasks must be idempotent (safe to retry)
- All tasks: `bind=True, max_retries=3`
- Use `self.retry(exc=e)` on transient errors
- Beat schedule lives in `celery_app.py`
- Two-phase pattern: `sync_parking_master_data` (daily) → `fetch_parking_availability` (every 2min)

## TDX API Notes

- Rate limit: 50,000 requests/day on free tier
- Auth: OAuth2 client credentials (token cached in Redis, expires in 1h)
- Base URL: `https://tdx.transportdata.tw/api/basic`
- Register: https://tdx.transportdata.tw

### Key Endpoints (Taichung)
```
Master data (daily):
  GET /v2/Parking/OffStreet/CarPark/City/Taichung
  GET /v2/Parking/OnStreet/Road/City/Taichung

Real-time (every 2–5 min):
  GET /v2/Parking/OffStreet/CarParkAvailability/City/Taichung
  GET /v2/Parking/OnStreet/RoadSectionAvailability/City/Taichung
```
