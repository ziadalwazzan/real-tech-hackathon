from datetime import datetime, timezone
import random
import re

from .schemas import Insight, Metric, RiskRequest, RiskResponse

ZIP_REGEX = re.compile(r"^\d{5}(-\d{4})?$")


def validate_location(payload: RiskRequest) -> bool:
    if payload.location_type == "zip":
        return bool(ZIP_REGEX.match(payload.query))
    return len(payload.query.strip()) > 1


def build_mock_response(payload: RiskRequest) -> RiskResponse:
    seed = sum(ord(ch) for ch in payload.query.lower())
    random.seed(seed)
    risk_score = random.randint(12, 88)

    if risk_score <= 33:
        level, color = "Low Risk", "green"
    elif risk_score <= 66:
        level, color = "Medium Risk", "yellow"
    else:
        level, color = "High Risk", "red"

    metrics = [
        Metric(
            name="Market Volatility",
            score=random.randint(20, 90),
            icon="trending-up",
            description="Stability of pricing and recent sales trends.",
        ),
        Metric(
            name="Neighborhood Safety",
            score=random.randint(25, 95),
            icon="shield",
            description="Crime trends and public safety indicators.",
        ),
        Metric(
            name="Economic Outlook",
            score=random.randint(30, 85),
            icon="briefcase",
            description="Employment growth and economic resilience.",
        ),
        Metric(
            name="Liquidity",
            score=random.randint(15, 80),
            icon="droplet",
            description="Expected time on market for similar properties.",
        ),
        Metric(
            name="Infrastructure",
            score=random.randint(35, 90),
            icon="map",
            description="Access to transit, schools, and amenities.",
        ),
    ]

    insights = [
        Insight(
            text="Balanced demand suggests moderate pricing pressure.",
            icon="sparkles",
        ),
        Insight(
            text="Safety indicators outperform metro averages.",
            icon="shield-check",
        ),
        Insight(
            text="Infrastructure upgrades planned within 12-18 months.",
            icon="rocket",
        ),
    ]

    location_label = (
        f"ZIP {payload.query}" if payload.location_type == "zip" else payload.query.title()
    )

    return RiskResponse(
        location=location_label,
        risk_score=risk_score,
        risk_level=level,
        color=color,
        metrics=metrics,
        insights=insights,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )
