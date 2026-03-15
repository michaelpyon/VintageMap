# VintageMap

Interactive web app that maps wine regions by vintage year. User picks a meaningful date → app shows a geographic heatmap of wine-producing regions → recommends a wine from that vintage with regional quality data.

## Tech stack

- **Frontend:** React 19, TypeScript, Vite, Leaflet + react-leaflet
- **Backend:** Python Flask, CORS, runs on port 5050
- **Architecture:** Flask serves API only; React frontend is a separate Vite dev server (or built static)

## Local dev

```bash
# Backend (terminal 1)
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python run.py           # runs on http://localhost:5050

# Frontend (terminal 2)
cd frontend
npm install
npm run dev             # Vite dev server, proxies API to localhost:5050
```

## Key files

- `backend/run.py` — Flask entry point
- `backend/app/__init__.py` — Flask factory, registers blueprints
- `backend/app/routes/vintage.py` — vintage year lookup endpoint
- `backend/app/routes/regions.py` — GeoJSON wine regions endpoint
- `backend/app/routes/recommend.py` — wine recommendation endpoint
- `backend/app/services/vintage_service.py` — year → region quality mapping logic
- `backend/app/services/recommendation.py` — recommendation ranking logic
- `backend/data/` — wine region data files (GeoJSON, vintage ratings)
- `frontend/src/App.tsx` — main orchestrator: date input → parallel fetch → map + card
- `frontend/src/api/client.ts` — HTTP client wrapping all backend endpoints
- `frontend/src/components/DateInput.tsx` — date picker
- `frontend/src/components/WineMap.tsx` — Leaflet map with region heatmap
- `frontend/src/components/RecommendationCard.tsx` — wine suggestion display
- `scripts/` — data prep / scraping scripts

## Architecture notes

- Date selection triggers parallel fetches: regions GeoJSON + wine recommendation
- UI scrolls to map section automatically after data loads
- `frontend/src/api/client.ts` uses `VITE_API_URL` env var (defaults to `/api` for production)
- Vite dev server proxies `/api` to Flask backend on port 5050 via `vite.config.ts`
- Service layer in `backend/app/services/` keeps business logic out of routes
- Dockerfile and railway.json configured for Railway deployment

## Deployment

- **Dockerfile:** 2-stage build (Node frontend → Python runtime with gunicorn)
- **railway.json:** Configured for Railway with auto-restart on failure
- Frontend builds to `static/` dir, served by Flask's catch-all route
