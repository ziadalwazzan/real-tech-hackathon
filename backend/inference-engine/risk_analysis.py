from __future__ import annotations

from typing import Sequence

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from scipy.optimize import minimize
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

from models import AssetSelection, RiskAnalysisOutputs


class RiskAnalysis:
    def __init__(
        self,
        df: pd.DataFrame,
        asset_names_or_number: AssetSelection,
        us_avg: pd.Series,
        risk_free_rate: float,
    ) -> None:
        if isinstance(asset_names_or_number, Sequence) and not isinstance(asset_names_or_number, (str, bytes)):
            self.data = df.loc[:, list(asset_names_or_number)]
        elif isinstance(asset_names_or_number, int):
            self.data = df.iloc[:, :asset_names_or_number]
        else:
            raise TypeError("asset_names_or_number must be a sequence of names or an integer")

        self.us_avg_data = us_avg
        self.returns = self.data.pct_change().dropna()
        self.correlation = self.returns.corr()
        self.distance = 1 - self.correlation
        self.us_avg_returns = self.us_avg_data.pct_change().dropna()
        self.cov_matrix = self.returns.cov()
        self.alpha_beta = self.get_alpha_and_beta()
        self.risk_free_rate = risk_free_rate
        self.expected_returns = self.get_expected_returns_CAPM()

    def to_outputs(self) -> RiskAnalysisOutputs:
        return RiskAnalysisOutputs(
            returns=self.returns,
            correlation=self.correlation,
            distance=self.distance,
            cov_matrix=self.cov_matrix,
            alpha_beta=self.alpha_beta,
            expected_returns=self.expected_returns,
        )

    def plot_correlation_matrix(self, figure_size: tuple[int, int] = (15, 15)) -> plt.Figure:
        fig = plt.figure(figsize=figure_size)
        sns.heatmap(
            self.correlation,
            annot=True,
            cmap="coolwarm",
            vmin=-1,
            vmax=1,
            center=0,
            fmt=".2f",
        )
        plt.title("Correlation (historic) Matrix of rent Returns")
        plt.tight_layout()
        plt.show()
        return fig

    def cluster_returns(self, n_clusters: int = 5) -> plt.Figure:
        kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=10)
        clusters = kmeans.fit_predict(self.distance)
        pca = PCA(n_components=2)
        reduced_data = pca.fit_transform(self.correlation)

        df_plot = pd.DataFrame(reduced_data, columns=["PC1", "PC2"])
        df_plot["City"] = self.correlation.columns
        df_plot["Cluster"] = clusters

        fig = plt.figure(figsize=(12, 8))
        sns.scatterplot(x="PC1", y="PC2", hue="Cluster", data=df_plot, palette="tab10", s=100)

        for i, city in enumerate(df_plot["City"]):
            plt.text(df_plot.iloc[i, 0] + 0.02, df_plot.iloc[i, 1], city, fontsize=9)

        plt.title("PCA of Housing Market Correlations", fontsize=15)
        plt.xlabel(f"PC1 (Explains {pca.explained_variance_ratio_[0]:.1%} of variance)")
        plt.ylabel(f"PC2 (Explains {pca.explained_variance_ratio_[1]:.1%} of variance)")
        plt.axvline(0, color="grey", linestyle="--", alpha=0.5)
        plt.axhline(0, color="grey", linestyle="--", alpha=0.5)
        sns.despine()
        plt.show()
        return fig

    def plot_season_variance(self) -> plt.Figure:
        features = []

        for city in self.data.columns:
            decomp = seasonal_decompose(self.data[city].dropna(), model="additive", period=12)
            trend = decomp.trend.dropna()
            seasonal = decomp.seasonal.dropna()
            mean_price = self.data[city].mean()

            trend_strength = trend.std() / mean_price
            season_strength = seasonal.std() / mean_price

            features.append(
                {
                    "City": city,
                    "Trend_Strength": trend_strength,
                    "Seasonal_Strength": season_strength,
                }
            )

        df_features = pd.DataFrame(features).set_index("City")

        kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
        df_features["Cluster"] = kmeans.fit_predict(df_features[["Trend_Strength", "Seasonal_Strength"]])

        fig = plt.figure(figsize=(10, 8))
        sns.scatterplot(
            data=df_features,
            x="Trend_Strength",
            y="Seasonal_Strength",
            hue="Cluster",
            palette="viridis",
            s=150,
            edgecolor="black",
        )

        for i in range(df_features.shape[0]):
            if (
                df_features.iloc[i].Trend_Strength > df_features.Trend_Strength.quantile(0.7)
                or df_features.iloc[i].Seasonal_Strength > df_features.Seasonal_Strength.quantile(0.7)
            ):
                plt.text(
                    df_features.iloc[i].Trend_Strength,
                    df_features.iloc[i].Seasonal_Strength,
                    df_features.index[i],
                    fontsize=9,
                )

        plt.title("Clustering Cities: Seasonality vs. Trend (Normalized)", fontsize=16)
        plt.xlabel("Trend Magnitude (as % of Price)")
        plt.ylabel("Seasonal Magnitude (as % of Price)")
        plt.grid(True, alpha=0.3)
        plt.show()
        return fig

    def plot_time_series_decompose(
        self,
        city_name: str,
        model: str = "additive",
        period: int = 12,
        bar_scaling_factor: int = 10,
    ) -> tuple[plt.Figure, tuple[float, float]]:
        data = self.data[city_name]
        if not isinstance(data.index, pd.DatetimeIndex):
            data.index = pd.to_datetime(data.index)

        result = seasonal_decompose(data, model=model, period=period)
        fig, axs = plt.subplots(4, 1, figsize=(12, 8), sharex=True)

        components = ["Observed", "Trend", "Seasonal", "Residual"]
        plot_data = [result.observed, result.trend, result.seasonal, result.resid]

        global_range = np.nanmax(result.observed) - np.nanmin(result.observed)
        bar_height = global_range / bar_scaling_factor

        year_locator = mdates.YearLocator()
        year_formatter = mdates.DateFormatter("%Y")

        for ax, comp, series in zip(axs, components, plot_data):
            ax.plot(series.index, series.values, marker="o", markersize=1, linewidth=1)
            ax.set_title(comp, fontsize=12, fontweight="bold")
            ax.grid(True, alpha=0.3)

            ax.xaxis.set_major_locator(year_locator)
            ax.xaxis.set_major_formatter(year_formatter)

            if len(series.dropna()) > 0:
                x_loc = series.index[-1]
                y_min, y_max = ax.get_ylim()
                y_loc = y_min + 0.05 * (y_max - y_min)

                ax.vlines(x=x_loc, ymin=y_loc, ymax=y_loc + bar_height, color="red", linewidth=2)
                ax.text(
                    x_loc,
                    y_loc + bar_height / 2,
                    f"{bar_height:.2e}",
                    color="red",
                    va="center",
                    ha="left",
                    fontsize=9,
                )

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        print("--- Stationarity Test (ADF) ---")
        result_adf = adfuller(data.dropna())
        print(f"ADF Statistic: {result_adf[0]:.4f}")
        print(f"p-value: {result_adf[1]:.4f}")
        if result_adf[1] < 0.05:
            print("Result: Likely Stationary")
        else:
            print("Result: Likely Non-Stationary")

        return fig, (result_adf[0], result_adf[1])

    def get_mean_monthly_prices(self, city_name: str) -> pd.Series:
        if city_name not in self.data.columns:
            raise ValueError(f"City not found: {city_name}")

        series = self.data[city_name].dropna()
        if not isinstance(series.index, pd.DatetimeIndex):
            series.index = pd.to_datetime(series.index)

        monthly_means = series.groupby(series.index.month).mean().round(0).astype(int)
        month_names = pd.to_datetime(monthly_means.index, format="%m").strftime("%b")
        monthly_means.index = month_names
        return monthly_means

    def get_alpha_and_beta(self) -> pd.DataFrame:
        results = {"Asset": [], "Alpha": [], "Beta": []}
        market_returns = self.us_avg_returns.rename("market")

        for asset in self.returns.columns:
            y = self.returns[asset]
            valid_data = pd.concat([y, market_returns], axis=1).dropna()

            if len(valid_data) < 2:
                results["Asset"].append(asset)
                results["Alpha"].append(np.nan)
                results["Beta"].append(np.nan)
                continue

            X_valid = sm.add_constant(valid_data["market"])
            y_valid = valid_data[asset]

            model = sm.OLS(y_valid, X_valid).fit()

            results["Asset"].append(asset)
            results["Alpha"].append(model.params["const"])
            results["Beta"].append(model.params["market"])

        results_CAPM = pd.DataFrame(results)
        return results_CAPM

    def plot_alpha_beta(self) -> plt.Figure:
        fig = plt.figure(figsize=(10, 6))
        for x in self.alpha_beta.index:
            asset_alpha = self.alpha_beta.loc[x, "Alpha"]
            asset_beta = self.alpha_beta.loc[x, "Beta"]
            plt.scatter([asset_alpha], [asset_beta], label=self.alpha_beta.loc[x, "Asset"])
            plt.text(
                asset_alpha,
                asset_beta,
                self.alpha_beta.loc[x, "Asset"],
                fontsize=6,
                ha="left",
                va="bottom",
            )
        plt.xlabel("alpha")
        plt.ylabel("beta")
        plt.title("alpha beta scatter plot")
        plt.grid(True)
        plt.show()
        return fig

    def get_expected_returns_CAPM(self) -> pd.Series:
        expected_market_return = self.us_avg_returns.mean()

        expected_returns = pd.Series(
            {
                asset: self.risk_free_rate
                + self.alpha_beta.loc[asset, "Beta"]
                * (expected_market_return - self.risk_free_rate)
                + self.alpha_beta.loc[asset, "Alpha"]
                for asset in self.alpha_beta.index
            }
        )
        return expected_returns

    def plot_efficient_frontier(self, n_points: int = 100) -> plt.Figure:
        if pd.api.types.is_integer_dtype(self.expected_returns.index):
            self.expected_returns.index = self.data.columns

        def get_portfolio_variance(weights: np.ndarray) -> float:
            return np.dot(weights.T, np.dot(self.cov_matrix, weights))

        def get_portfolio_return(weights: np.ndarray) -> float:
            return np.sum(self.expected_returns * weights)

        def minimize_volatility(weights: np.ndarray) -> float:
            return np.sqrt(get_portfolio_variance(weights))

        n_assets = len(self.expected_returns)
        bounds = tuple((0, 1) for _ in range(n_assets))
        initial_guess = np.array([1 / n_assets] * n_assets)

        min_ret = self.expected_returns.min()
        max_ret = self.expected_returns.max()
        target_returns = np.linspace(min_ret, max_ret - 1e-6, n_points)

        efficient_volatilities: list[float] = []
        efficient_returns: list[float] = []

        for target in target_returns:
            constraints = (
                {"type": "eq", "fun": lambda w: np.sum(w) - 1},
                {"type": "eq", "fun": lambda w: get_portfolio_return(w) - target},
            )

            result = minimize(
                minimize_volatility,
                initial_guess,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
                options={"maxiter": 1000},
            )

            if result.success:
                efficient_volatilities.append(result.fun)
                efficient_returns.append(target)

        fig = plt.figure(figsize=(12, 8))

        if len(efficient_volatilities) > 0:
            plt.plot(
                efficient_volatilities,
                efficient_returns,
                "k--",
                linewidth=2,
                label="Efficient Frontier",
            )
        else:
            print("Warning: Optimizer failed to find the frontier. Check data for NaNs.")

        asset_vols = np.sqrt(np.diag(self.cov_matrix))
        sns.scatterplot(x=asset_vols, y=self.expected_returns, s=80, color="#1f77b4", zorder=2)

        for name, vol, ret in zip(self.expected_returns.index, asset_vols, self.expected_returns):
            plt.text(
                vol + (max(asset_vols) * 0.01),
                ret,
                str(name),
                fontsize=9,
                ha="left",
                va="center",
            )

        market_vol = self.us_avg_returns.std()
        market_ret = self.us_avg_returns.mean()
        if isinstance(market_vol, pd.Series):
            market_vol = market_vol.iloc[0]
            market_ret = market_ret.iloc[0]

        plt.scatter(market_vol, market_ret, c="red", s=150, marker="*", label="Market Avg", zorder=3)
        plt.text(market_vol, market_ret, "  Market", color="red", fontweight="bold", ha="left")

        plt.title("Efficient Frontier (Markowitz Portfolio Optimization)", fontsize=16)
        plt.xlabel("Risk (Volatility)", fontsize=12)
        plt.ylabel("Return (Expected)", fontsize=12)
        plt.legend(loc="best")
        plt.grid(True, alpha=0.3)
        sns.despine()
        plt.show()
        return fig

    def top_cities_with_better_return_at_risk(
        self,
        city_name: str,
        top_n: int = 3,
    ) -> list[tuple[str, float, float]]:
        if pd.api.types.is_integer_dtype(self.expected_returns.index):
            self.expected_returns.index = self.data.columns

        if city_name not in self.data.columns:
            raise ValueError(f"City not found: {city_name}")

        asset_vols = pd.Series(np.sqrt(np.diag(self.cov_matrix)), index=self.data.columns)
        target_risk = asset_vols.loc[city_name]
        target_return = float(self.expected_returns.loc[city_name])

        eligible = asset_vols[asset_vols <= target_risk].index
        better = self.expected_returns.loc[eligible]
        better = better[better > target_return].sort_values(ascending=False)

        risk_min = float(asset_vols.min())
        risk_max = float(asset_vols.max())
        risk_denom = risk_max - risk_min

        return_min = float(self.expected_returns.min())
        return_max = float(self.expected_returns.max())
        return_denom = return_max - return_min

        results: list[tuple[str, float, float]] = []

        if risk_denom == 0:
            target_scaled_risk = 0.0
        else:
            target_scaled_risk = (target_risk - risk_min) / risk_denom * 100.0

        if return_denom == 0:
            target_scaled_return = 0.0
        else:
            target_scaled_return = (target_return - return_min) / return_denom * 100.0

        results.append((city_name, round(target_scaled_risk, 2), round(target_scaled_return, 2)))
        for name in better.index[:top_n]:
            raw_risk = float(asset_vols.loc[name])
            if risk_denom == 0:
                scaled_risk = 0.0
            else:
                scaled_risk = (raw_risk - risk_min) / risk_denom * 100.0

            raw_return = float(self.expected_returns.loc[name])
            if return_denom == 0:
                scaled_return = 0.0
            else:
                scaled_return = (raw_return - return_min) / return_denom * 100.0

            results.append((name, round(scaled_risk, 2), round(scaled_return, 2)))

        return results


risk_analysis = RiskAnalysis
