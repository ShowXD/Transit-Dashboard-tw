# 台中停車場即時儀表板

> 即時顯示台中市路外停車場與路邊停車路段的剩餘車位，
> 資料來源為 [TDX 運輸資料流通服務](https://tdx.transportdata.tw)。

[![CI](https://github.com/ShowXD/transit-dashboard-tw/actions/workflows/ci.yml/badge.svg)](https://github.com/ShowXD/transit-dashboard-tw/actions/workflows/ci.yml)

---

## 這個專案做什麼

- **Leaflet.js 地圖**：每個停車場用彩色圓點標示（綠＝充裕、黃＝緊張、紅＝接近滿位）
- **即時資料**：Celery 定期向 TDX API 拉取，路外停車場每 2 分鐘更新
- **可收合側欄**：顯示統計數字與停車場列表，Navbar 左側按鈕可開關
- **地理過濾**：API 支援以經緯度 + 半徑搜尋附近停車場

---

## 技術棧

| 層級 | 技術 |
| --- | --- |
| Backend API | FastAPI + Python 3.12 |
| 資料庫 | PostgreSQL 15 |
| 排程 / 任務佇列 | Celery + Redis |
| Frontend | Vue 3 + Vite + Leaflet.js |
| 容器化 | Docker Compose |
| 部署 | Railway（計畫中） |

---

## 快速啟動

### 事前準備

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)（本機不需要安裝 Node.js 或 Python）
- TDX API 帳號（[免費申請](https://tdx.transportdata.tw)，需另外申請「停車」資料使用權限）

### 步驟

```bash
# 1. Clone 專案
git clone https://github.com/ShowXD/transit-dashboard-tw.git
cd transit-dashboard-tw

# 2. 設定環境變數
cp backend/.env.example backend/.env
# 開啟 backend/.env，填入 TDX_CLIENT_ID 和 TDX_CLIENT_SECRET

# 3. 啟動所有服務（API + DB + Redis + Celery + 前端）
docker compose up -d

# 4. 執行資料庫 migration（第一次執行）
docker compose exec api alembic upgrade head

# 5. 觸發首次資料同步（需 TDX 停車 API 權限）
docker compose exec celery sh -c \
  "celery -A app.workers.celery_app call app.workers.tasks.sync_parking_master_data"
```

### 服務位址

| 服務 | URL |
| --- | --- |
| **前端儀表板** | <http://localhost:5173> |
| **API 文件（Swagger）** | <http://localhost:8000/docs> |
| Health check | <http://localhost:8000/health> |

---

## TDX API 設定

TDX 免費帳號預設**不包含停車資料**，需額外申請：

1. 登入 [tdx.transportdata.tw](https://tdx.transportdata.tw)
2. 進入「會員中心」→「資料申請」→ 申請「**停車 (Parking)**」類別
3. 審核通過後，在「API 金鑰管理」取得 `Client ID` / `Client Secret`
4. 填入 `backend/.env`，執行 `docker compose up -d api celery` 重啟生效

> **尚未取得 TDX 權限？** 可執行 seed script 塞假資料測試前端：
> `docker compose exec api python scripts/seed_demo.py`

---

## 架構

```text
TDX API ──OAuth2──▶ Celery Worker (每 2–5 分鐘)
                           │ UPSERT
                           ▼
                      PostgreSQL
               parking_lots / availability
               road_sections / availability
                           │ async SQLAlchemy
                           ▼
            FastAPI ──▶ Vue 3 SPA (Leaflet.js)
                           │
                    Redis（TDX token 快取）
```

---

## API 端點

| 端點 | 說明 |
| --- | --- |
| `GET /api/v1/parking/lots` | 路外停車場 + 即時車位 |
| `GET /api/v1/parking/lots/{id}` | 單一停車場詳細資訊 |
| `GET /api/v1/parking/road-sections` | 路邊停車路段 + 即時車位 |

地理搜尋範例：`/api/v1/parking/lots?lat=24.148&lon=120.674&radius_m=1000`

---

## 常用指令

```bash
# 查看 log
docker compose logs -f api
docker compose logs -f celery

# 修改 .env 後重啟（需 up -d，不能只 restart）
docker compose up -d api celery

# 執行測試
docker compose exec api pytest -v
```

---

## 已知問題

| 問題 | 原因 | 解法 |
| --- | --- | --- |
| 修改前端後畫面沒更新 | Windows Docker volume 不支援 inotify，HMR 無效 | **Ctrl+Shift+R** 強制重整 |
| `restart` 後環境變數沒更新 | `restart` 不重新讀取 env\_file | 改用 `docker compose up -d <service>` |
| TDX API 全部回 404 | 帳號未申請停車資料權限 | 見上方 TDX API 設定說明 |

---

## License

MIT © Xue Yi-Zhan
