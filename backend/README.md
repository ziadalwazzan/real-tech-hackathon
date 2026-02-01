# Backend (FastAPI)

## Setup
Use Python 3.12 (pydantic-core does not support 3.14 yet).
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints
- `GET /health`
- `POST /risk-assessment`

Example request:
```json
{
  "query": "90210",
  "location_type": "zip"
}
```

Example response:
```json
{
  "location": "ZIP 90210",
  "risk_score": 42,
  "risk_level": "Medium Risk",
  "color": "yellow",
  "metrics": [
    {
      "name": "Market Volatility",
      "score": 58,
      "icon": "trending-up",
      "description": "Stability of pricing and recent sales trends."
    }
  ],
  "insights": [
    {
      "text": "Balanced demand suggests moderate pricing pressure.",
      "icon": "sparkles"
    }
  ],
  "generated_at": "2026-01-31T12:00:00+00:00"
}
```

Swagger UI: http://localhost:8000/docs
Redoc: http://localhost:8000/redoc
