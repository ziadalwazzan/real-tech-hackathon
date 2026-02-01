from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence, Union, TYPE_CHECKING

import pandas as pd

AssetSelection = Union[Sequence[str], int]


@dataclass(frozen=True)
class RiskAnalysisInputs:
    data: pd.DataFrame
    asset_names_or_number: AssetSelection
    us_avg: pd.Series
    risk_free_rate: float


@dataclass
class RiskAnalysisOutputs:
    returns: pd.DataFrame
    correlation: pd.DataFrame
    distance: pd.DataFrame
    cov_matrix: pd.DataFrame
    alpha_beta: pd.DataFrame
    expected_returns: pd.Series


if TYPE_CHECKING:
    from .risk_analysis import RiskAnalysis


@dataclass(frozen=True)
class MarketArbitrageInputs:
    rent_analysis: "RiskAnalysis"
    price_analysis: "RiskAnalysis"


@dataclass
class MarketArbitrageOutputs:
    price_rent_corr: pd.Series
    latest_valuation: Optional[pd.DataFrame] = None
