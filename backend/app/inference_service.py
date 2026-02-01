from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import sys
from typing import List


_INFERENCE_DIR = Path(__file__).resolve().parents[1] / "inference-engine"
if str(_INFERENCE_DIR) not in sys.path:
    sys.path.append(str(_INFERENCE_DIR))

from datasets import load_default_datasets
from risk_analysis import RiskAnalysis


@lru_cache(maxsize=1)
def _get_rent_analysis() -> RiskAnalysis:
    datasets = load_default_datasets()
    return RiskAnalysis(
        df=datasets.rent_ts,
        asset_names_or_number=list(datasets.rent_ts.columns),
        us_avg=datasets.us_avg_rent,
        risk_free_rate=0.0,
    )


def get_top_cities_with_better_return_at_risk(city_name: str, top_n: int = 3) -> List[tuple[str, float, float]]:
    analysis = _get_rent_analysis()
    return analysis.top_cities_with_better_return_at_risk(city_name, top_n=top_n)


def get_mean_monthly_prices(city_name: str) -> List[tuple[str, int]]:
    analysis = _get_rent_analysis()
    series = analysis.get_mean_monthly_prices(city_name)
    return [(month, int(value)) for month, value in series.items()]
