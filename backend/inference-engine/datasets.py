from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class DatasetBundle:
    rent_ts: pd.DataFrame
    value_ts: pd.DataFrame
    us_avg_rent: pd.Series
    us_avg_value: pd.Series


def _default_dataset_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "datasets"


def _load_city_timeseries(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    df_t = df.T
    df_ts = df_t.iloc[8:, :]
    df_ts.columns = df_t.loc["RegionName"].astype(str) + " (" + df["State"].astype(str) + ")"

    df_ts = df_ts.astype(float)
    df_ts = df_ts.loc[:, df_ts.isna().sum() <= 10]
    df_ts_filtered = df_ts.loc[:, df_ts.isna().sum() <= 15]
    df_ts_filtered = df_ts_filtered.interpolate(method="linear")
    return df_ts_filtered


def load_city_rent_timeseries(dataset_dir: Path | None = None) -> pd.DataFrame:
    base_dir = dataset_dir or _default_dataset_dir()
    return _load_city_timeseries(base_dir / "US_rental_city.csv")


def load_city_value_timeseries(dataset_dir: Path | None = None) -> pd.DataFrame:
    base_dir = dataset_dir or _default_dataset_dir()
    return _load_city_timeseries(base_dir / "US_value_city.csv")


def _load_us_avg_series(csv_path: Path) -> pd.Series:
    df = pd.read_csv(csv_path)
    series = pd.Series(df.iloc[:, 1].values, index=df.iloc[:, 0])
    return series


def load_us_avg_rent_series(dataset_dir: Path | None = None) -> pd.Series:
    base_dir = dataset_dir or _default_dataset_dir()
    return _load_us_avg_series(base_dir / "US_avg.csv")


def load_us_avg_value_series(dataset_dir: Path | None = None) -> pd.Series:
    base_dir = dataset_dir or _default_dataset_dir()
    return _load_us_avg_series(base_dir / "US_value_avg.csv")


def load_default_datasets(dataset_dir: Path | None = None) -> DatasetBundle:
    base_dir = dataset_dir or _default_dataset_dir()
    return DatasetBundle(
        rent_ts=load_city_rent_timeseries(base_dir),
        value_ts=load_city_value_timeseries(base_dir),
        us_avg_rent=load_us_avg_rent_series(base_dir),
        us_avg_value=load_us_avg_value_series(base_dir),
    )
