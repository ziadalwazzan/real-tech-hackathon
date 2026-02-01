from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .schemas import FrontierResponse, RiskRequest, RiskResponse, SeasonalPricesResponse
from .data import build_mock_response, validate_location
from .inference_service import get_mean_monthly_prices, get_top_cities_with_better_return_at_risk

app = FastAPI(
    title="Real Estate Risk Assessment API",
    version="0.1.0",
    description="Mock API for real estate investment risk assessment",
)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok"}


@app.post("/risk-assessment", response_model=RiskResponse)
async def risk_assessment(payload: RiskRequest) -> RiskResponse:
    if not validate_location(payload):
        raise HTTPException(status_code=400, detail="Invalid location input")
    return build_mock_response(payload)


@app.get("/frontier-comparables", response_model=FrontierResponse)
async def frontier_comparables(city: str, top_n: int = 3) -> FrontierResponse:
    if len(city.strip()) < 2:
        raise HTTPException(status_code=400, detail="City name too short")

    try:
        results = get_top_cities_with_better_return_at_risk(city, top_n=top_n)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return FrontierResponse(
        results=[
            {"city": name, "risk_score": risk_score, "return_score": return_score}
            for name, risk_score, return_score in results
        ]
    )


@app.get("/seasonal-prices", response_model=SeasonalPricesResponse)
async def seasonal_prices(city: str) -> SeasonalPricesResponse:
    if len(city.strip()) < 2:
        raise HTTPException(status_code=400, detail="City name too short")

    try:
        monthly = get_mean_monthly_prices(city)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return SeasonalPricesResponse(
        city=city,
        monthly=[{"month": month, "value": value} for month, value in monthly],
    )
