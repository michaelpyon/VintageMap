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
- **IMPORTANT:** `frontend/src/api/client.ts` hardcodes `http://localhost:5050/api` — needs an env var for production deployment
- Service layer in `backend/app/services/` keeps business logic out of routes
- No deployment config exists yet (no Dockerfile, no railway.json) — needs to be built if deploying

## Deployment status

**Not deployed.** No Dockerfile or Railway config exists. To deploy:
1. Add env var support to `frontend/src/api/client.ts` for `VITE_API_URL`
2. Write a Dockerfile (similar pattern to subway-shame: Node build stage + Python runtime stage)
3. Set up Railway or Render project
