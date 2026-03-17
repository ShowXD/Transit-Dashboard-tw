# Taichung Parking Dashboard 台中停車場即時資訊

> Real-time parking availability dashboard for Taichung City — off-street lots and on-street road sections, powered by the [TDX API](https://tdx.transportdata.tw).

[![CI](https://github.com/ShowXD/transit-dashboard-tw/actions/workflows/ci.yml/badge.svg)](https://github.com/ShowXD/transit-dashboard-tw/actions/workflows/ci.yml)

---

## What It Does

This platform ingests real-time parking availability data from Taiwan's open transport API (TDX) every 2–5 minutes, persists it to PostgreSQL, and exposes a REST API consumed by an interactive Vue 3 + Leaflet.js map dashboard.

| Feature | Data Source | Update Frequency |
|---------|------------|-----------------|
| 路外停車場即時車位 Off-street lots | TDX Parking API | every 2 min |
| 路邊停車路段即時車位 On-street road sections | TDX Parking API | every 5 min |

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Backend API | **FastAPI** + Python 3.12 | Async-first, auto-generated OpenAPI docs |
| Database | **PostgreSQL 15** | Relational integrity, geospatial-ready |
| Task Queue | **Celery** + **Redis** | Scheduled TDX polling with retry logic |
| Frontend | **Vue 3** + Vite + **Leaflet.js** | Interactive map with live availability pins |
| Containerization | Docker Compose | One-command local dev environment |
| Deployment | **Railway** | Free-tier hosting for portfolio |

---

## Architecture

```
┌──────────────┐   OAuth2    ┌──────────────────────┐
│   TDX API    │◄────────────│   Celery Worker      │
│ (open data)  │  2–5 min    │   + Beat Scheduler   │
└──────────────┘             └──────────┬───────────┘
                                        │ UPSERT
                             ┌──────────▼───────────┐
                             │      PostgreSQL       │
                             │  parking_lots         │
                             │  parking_availability │
                             │  road_sections        │
                             │  road_availability    │
                             └──────────┬───────────┘
                                        │ SQLAlchemy async
                             ┌──────────▼───────────┐     ┌─────────────────┐
                             │       FastAPI         │────►│   Vue 3 SPA     │
                             │   /api/v1/parking/... │     │ + Leaflet.js    │
                             └───────────────────────┘     │  map + markers  │
                                        │                  └─────────────────┘
                             ┌──────────▼───────────┐
                             │        Redis          │
                             │   (hot cache TTL)     │
                             └───────────────────────┘
```

---

## Quick Start

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Node.js 20+ (for frontend dev server)
- TDX API credentials — [free registration here](https://tdx.transportdata.tw)

### Run Locally

```bash
# 1. Clone and configure
git clone https://github.com/ShowXD/transit-dashboard-tw.git
cd transit-dashboard-tw
cp backend/.env.example backend/.env
# Edit backend/.env → fill in TDX_CLIENT_ID and TDX_CLIENT_SECRET

# 2. Start all backend services (api + db + redis + celery)
docker compose up -d

# 3. Run database migrations
docker compose exec api alembic upgrade head

# 4. Start frontend dev server (separate terminal)
cd frontend
npm install
npm run dev
```

| Service | URL |
|---------|-----|
| FastAPI (Swagger) | http://localhost:8000/docs |
| FastAPI (ReDoc) | http://localhost:8000/redoc |
| Frontend | http://localhost:5173 |
| Health check | http://localhost:8000/health |

---

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Service health check |
| `/api/v1/parking/lots` | GET | Off-street lots with real-time availability |
| `/api/v1/parking/lots/{id}` | GET | Single lot detail + availability |
| `/api/v1/parking/road-sections` | GET | On-street sections with availability |

Query params for map proximity search: `?lat=24.148&lon=120.674&radius_m=1000`

---

## Database Schema

```
parking_lots       (id, external_id, name, car_park_type, lat, lon, total_spaces, ...)
    │
    └── parking_availability  (lot_id→, available_spaces, updated_at)

road_sections      (id, external_id, road_name, lat, lon, total_spaces, ...)
    │
    └── road_availability     (section_id→, available_spaces, updated_at)
```

All availability tables use `INSERT ... ON CONFLICT DO UPDATE` (upsert) for idempotent Celery writes.

---

## Project Phases

| Phase | Branch | Description | Status |
|-------|--------|-------------|--------|
| 1 | `feat/db-schema` | Project skeleton + Docker + DB schema | ✅ Done |
| 2 | `feat/tdx-fetcher` | TDX OAuth2 client + Celery fetch tasks | 🔄 Next |
| 3 | `feat/api-routes` | Full API with proximity search + Redis cache | ⏳ Planned |
| 4 | `feat/frontend-dashboard` | Vue map + availability markers | ⏳ Planned |

---

## License

MIT © Xue Yi-Zhan
