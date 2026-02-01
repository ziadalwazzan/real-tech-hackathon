from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from datasets import load_default_datasets
from market_arbitrage import MarketArbitrage
from risk_analysis import RiskAnalysis


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    output_dir = base_dir / "_tmp_outputs"
    output_dir.mkdir(exist_ok=True)

    datasets = load_default_datasets()

    rent_analysis = RiskAnalysis(
        df=datasets.rent_ts,
        asset_names_or_number=list(datasets.rent_ts.columns),
        us_avg=datasets.us_avg_rent,
        risk_free_rate=0.0,
    )
    price_analysis = RiskAnalysis(
        df=datasets.value_ts,
        asset_names_or_number=35,
        us_avg=datasets.us_avg_value,
        risk_free_rate=0.0,
    )

    results = rent_analysis.top_cities_with_better_return_at_risk("Denver (CO)")
    print("Top 3:", results)

    monthly = rent_analysis.get_mean_monthly_prices("Austin (TX)")
    print(monthly)


if __name__ == "__main__":
    main()
