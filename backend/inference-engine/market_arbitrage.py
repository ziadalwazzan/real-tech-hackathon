from __future__ import annotations

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression

from models import MarketArbitrageOutputs
from risk_analysis import RiskAnalysis


class MarketArbitrage:
    def __init__(self, rent_obj: RiskAnalysis, price_obj: RiskAnalysis) -> None:
        self.rent_obj = rent_obj
        self.price_obj = price_obj

        self.rents = rent_obj.data
        self.prices = price_obj.data
        self.rents_returns = rent_obj.returns
        self.prices_returns = price_obj.returns

        self.price_rent_corr = self.prices_returns.corrwith(self.rents_returns)
        self.latest_valuation: pd.DataFrame | None = None

    def to_outputs(self) -> MarketArbitrageOutputs:
        return MarketArbitrageOutputs(
            price_rent_corr=self.price_rent_corr,
            latest_valuation=self.latest_valuation,
        )

    def plot_correlation_rent_value(self) -> plt.Figure:
        correlations = self.price_rent_corr.sort_values()

        fig = plt.figure(figsize=(10, max(6, len(correlations) * 0.25)))
        sns.barplot(x=correlations.values, y=correlations.index)

        plt.title("Correlation: Home Prices vs. Rents", fontsize=16)
        plt.xlabel("Correlation Coefficient (Pearson)", fontsize=12)
        plt.axvline(0, color="black", linewidth=1)
        plt.grid(axis="x", linestyle="--", alpha=0.5)
        sns.despine()

        plt.show()
        return fig

    def plot_cross_sectional_valuation(self, date_index: int = -1) -> pd.DataFrame:
        latest_prices = self.prices.iloc[date_index]
        latest_rents = self.rents.iloc[date_index]

        latest_prices = latest_prices[~latest_prices.index.duplicated(keep="first")]
        latest_rents = latest_rents[~latest_rents.index.duplicated(keep="first")]

        df = pd.DataFrame({"Price": latest_prices, "Rent": latest_rents}).dropna()

        X = df[["Rent"]]
        y = df["Price"]

        model = LinearRegression()
        model.fit(X, y)

        df["Predicted_Price"] = model.predict(X)
        df["Mispricing"] = df["Price"] - df["Predicted_Price"]
        df["Z_Score"] = (df["Mispricing"] - df["Mispricing"].mean()) / df["Mispricing"].std()

        self.latest_valuation = df

        df_sorted = df.sort_values("Z_Score")
        plt.figure(figsize=(12, max(6, len(df_sorted) * 0.25)))
        colors = [
            "#d62728" if z > 1 else "#2ca02c" if z < -1 else "lightgrey" for z in df_sorted["Z_Score"]
        ]

        sns.barplot(x=df_sorted["Z_Score"], y=df_sorted.index, palette=colors)

        plt.axvline(0, color="black", linestyle="--")
        plt.axvline(1, color="red", linestyle=":", label="Overvalued (>1σ)")
        plt.axvline(-1, color="green", linestyle=":", label="Undervalued (<-1σ)")

        plt.title("Cross-Sectional Valuation: Which Cities are Cheap vs. Rents?", fontsize=16)
        plt.xlabel("Z-Score (Standard Deviations from Fair Value)")
        plt.legend()
        sns.despine()
        plt.tight_layout()
        plt.show()

        return df

    def analyze_historical_fair_value(self, city_name: str, window: int | None = None) -> None:
        if city_name not in self.prices.columns or city_name not in self.rents.columns:
            print(f"Error: {city_name} not found.")
            return

        ts_price = self.prices[city_name]
        ts_rent = self.rents[city_name]

        df = pd.concat([ts_price, ts_rent], axis=1).dropna()
        df.columns = ["Price", "Rent"]
        df["Ratio"] = df["Price"] / df["Rent"]

        if window:
            mean_ratio = df["Ratio"].rolling(window=window).mean()
            std_ratio = df["Ratio"].rolling(window=window).std()
            label_txt = f"{window}-Month Moving Avg"
        else:
            mean_ratio = df["Ratio"].mean()
            std_ratio = df["Ratio"].std()
            label_txt = "Historical Mean"

        upper = mean_ratio + (2 * std_ratio)
        lower = mean_ratio - (2 * std_ratio)

        plt.figure(figsize=(12, 6))
        df.index = pd.to_datetime(df.index)

        plt.plot(df.index, df["Ratio"], label="Price/Rent Ratio", color="#1f77b4")

        if window:
            plt.plot(df.index, mean_ratio, color="black", linestyle="--", label=label_txt)
            plt.fill_between(df.index, lower, upper, color="gray", alpha=0.1)
        else:
            plt.axhline(mean_ratio, color="black", linestyle="--", label=label_txt)
            plt.axhspan(lower, upper, color="gray", alpha=0.1)

        ax = plt.gca()
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        plt.gcf().autofmt_xdate()
        plt.title(f"{city_name}: Price-to-Rent Mean Reversion", fontsize=16)
        plt.legend()
        sns.despine()
        plt.show()

    def scan_for_opportunities(self, correlation_threshold: float = 0.5) -> pd.DataFrame:
        if self.latest_valuation is None:
            print("Running valuation model first...")
            self.plot_cross_sectional_valuation()

        opportunities = self.latest_valuation.copy()
        opportunities["Correlation"] = self.price_rent_corr

        valid_opps = opportunities[opportunities["Correlation"] > correlation_threshold].sort_values("Z_Score")

        print(f"--- Top Opportunities (Corr > {correlation_threshold}) ---")
        print(valid_opps[["Z_Score", "Correlation", "Price", "Rent"]].head())
        print("\n--- Top Risks (Overvalued) ---")
        print(valid_opps[["Z_Score", "Correlation", "Price", "Rent"]].tail())

        return valid_opps
