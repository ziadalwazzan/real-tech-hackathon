"""Inference engine package for dataset-backed analytics."""

from .models import (
    AssetSelection,
    MarketArbitrageInputs,
    MarketArbitrageOutputs,
    RiskAnalysisInputs,
    RiskAnalysisOutputs,
)
from .risk_analysis import RiskAnalysis, risk_analysis
from .market_arbitrage import MarketArbitrage
from .datasets import (
    DatasetBundle,
    load_city_rent_timeseries,
    load_city_value_timeseries,
    load_us_avg_rent_series,
    load_us_avg_value_series,
    load_default_datasets,
)

__all__ = [
    "AssetSelection",
    "MarketArbitrage",
    "MarketArbitrageInputs",
    "MarketArbitrageOutputs",
    "RiskAnalysis",
    "RiskAnalysisInputs",
    "RiskAnalysisOutputs",
    "risk_analysis",
    "DatasetBundle",
    "load_city_rent_timeseries",
    "load_city_value_timeseries",
    "load_us_avg_rent_series",
    "load_us_avg_value_series",
    "load_default_datasets",
]
