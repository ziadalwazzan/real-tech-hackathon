# Real Estate Risk Assessment App (MVP)

Mobile-first web UI + mock API for real estate investment risk assessment. Data modeling and risk algorithms are mocked for now.

## Structure
```
backend/   FastAPI app (mock API + schemas)
frontend/  React app (Tailwind UI + routing)
```

## Quick Start
### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## MVP Flow
1. Enter ZIP or City on Home
2. Loading state
3. Results dashboard

## Notes
- CORS enabled for localhost dev servers.
- Mock responses only; no persistence.
- API docs: http://localhost:8000/docs
