from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, model_validator


class LocationType(str, Enum):
    zip = "zip"
    city = "city"


class RiskRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=64)
    location_type: LocationType

    @model_validator(mode="after")
    def normalize_query(self) -> "RiskRequest":
        self.query = self.query.strip()
        return self


class Metric(BaseModel):
    name: str
    score: int = Field(..., ge=0, le=100)
    icon: str
    description: str


class Insight(BaseModel):
    text: str
    icon: str


class RiskResponse(BaseModel):
    location: str
    risk_score: int = Field(..., ge=0, le=100)
    risk_level: str
    color: str
    metrics: List[Metric]
    insights: List[Insight]
    generated_at: str


class FrontierComparable(BaseModel):
    city: str
    risk_score: float = Field(..., ge=0, le=100)
    return_score: float = Field(..., ge=0, le=100)


class FrontierResponse(BaseModel):
    results: List[FrontierComparable]


class SeasonalPricePoint(BaseModel):
    month: str
    value: int


class SeasonalPricesResponse(BaseModel):
    city: str
    monthly: List[SeasonalPricePoint]
