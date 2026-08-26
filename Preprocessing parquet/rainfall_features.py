"""
rainfall_features.py
---------------------
Turns the 2018-2025 IMD RF25 NetCDF files into a per-grid-cell, per-day
feature table: rolling accumulations, climatological anomaly, intensity,
and wet-spell stats.

Run standalone:  python rainfall_features.py
"""

import numpy as np
import pandas as pd
import xarray as xr

from config import (
    RAINFALL_DIR,
    RAINFALL_FEATURES_PARQUET,
    ROLLING_WINDOWS_DAYS,
    WET_DAY_THRESHOLD_MM,
    EXTREME_PERCENTILE,
    get_dem_bbox,
)
from grid_utils import build_reference_grid, filter_to_bbox, make_grid_id


def _find_rain_var(ds: xr.Dataset) -> str:
    """
    IMD RF25 files sometimes name the rainfall variable differently
    (RAINFALL, rf, precip...). Pick the first data variable that has a
    time-like dimension rather than hardcoding a name.
    """
    for name, da in ds.data_vars.items():
        if any(d.lower() in ("time",) for d in da.dims):
            return name
    # fallback: just take the first data var
    return list(ds.data_vars)[0]


def load_rainfall_dataset(rainfall_dir=RAINFALL_DIR) -> xr.Dataset:
    """
    Opens every RF25_ind{year}_rfp25.nc file and concatenates along time.
    Uses open_mfdataset so this stays memory-safe even across 8 years.
    """
    files = sorted(rainfall_dir.glob("RF25_ind*_rfp25.nc"))
    if not files:
        raise FileNotFoundError(f"No RF25_ind*_rfp25.nc files found in {rainfall_dir}")

    print(f"Opening {len(files)} rainfall files: {[f.name for f in files]}")
    ds = xr.open_mfdataset(files, combine="by_coords", chunks={"TIME": 365})

    # normalize dim/coord names across possible IMD export variants
    rename_map = {}
    for a, b in [("TIME", "time"), ("LATITUDE", "lat"), ("LONGITUDE", "lon")]:
        if a in ds.coords or a in ds.dims:
            rename_map[a] = b
    ds = ds.rename(rename_map) if rename_map else ds
    return ds


def compute_rainfall_features(ds: xr.Dataset, bbox=None) -> pd.DataFrame:
    """
    Core feature computation, done in xarray (lazy/chunked) before dropping
    to pandas, so this scales to the full 2018-2025 period without blowing
    up memory.
    """
    var = _find_rain_var(ds)
    rain = ds[var]

    if bbox is not None:
        lat_min, lat_max, lon_min, lon_max = bbox
        rain = rain.sel(lat=slice(lat_min, lat_max), lon=slice(lon_min, lon_max))
        print(f"Clipped rainfall to DEM bbox: lat[{lat_min},{lat_max}] lon[{lon_min},{lon_max}]")

    # rolling accumulations
    features = {"rainfall_1d": rain}
    for w in ROLLING_WINDOWS_DAYS:
        if w == 1:
            continue
        features[f"rainfall_{w}d"] = rain.rolling(time=w, min_periods=1).sum()

    # max intensity within the 7-day window (captures a single sharp burst
    # even if the multi-day total looks moderate)
    features["max_intensity_7d"] = rain.rolling(time=7, min_periods=1).max()

    # wet-spell length: consecutive days above threshold, reset on dry days
    is_wet = (rain >= WET_DAY_THRESHOLD_MM).astype(int)
    # cumulative count that resets at each zero — computed cell-by-cell in pandas
    # below since xarray has no native "reset on zero" cumsum.

    # rainy days in trailing 30-day window
    features["rainy_days_30d"] = is_wet.rolling(time=30, min_periods=1).sum()

    # climatological anomaly: per-cell, per-calendar-month z-score
    monthly_mean = rain.groupby("time.month").mean("time")
    monthly_std = rain.groupby("time.month").std("time").where(lambda s: s > 0, 1.0)
    anomaly = xr.apply_ufunc(
        lambda r, m, s: (r - m) / s,
        rain.groupby("time.month"),
        monthly_mean,
        monthly_std,
        dask="allowed",
    )
    features["rainfall_anomaly_z"] = anomaly

    ds_feat = xr.Dataset(features)
    df = ds_feat.to_dataframe().reset_index()
    df = df.rename(columns={var: "rainfall_1d"} if var != "rainfall_1d" else {})

    df["grid_id"] = make_grid_id(df["lat"], df["lon"])
    df["date"] = pd.to_datetime(df["time"]).dt.date
    df = df.drop(columns=["time"])

    # wet-spell length: reset-on-zero cumulative count, done per grid cell in pandas
    df = df.sort_values(["grid_id", "date"])
    wet = (df["rainfall_1d"] >= WET_DAY_THRESHOLD_MM).astype(int)
    grp = df.groupby("grid_id")["rainfall_1d"].transform(lambda s: (s < WET_DAY_THRESHOLD_MM))
    reset_id = grp.groupby(df["grid_id"]).cumsum()
    df["wet_spell_length"] = wet.groupby([df["grid_id"], reset_id]).cumsum() * wet

    # simple extreme-rain flag: per-cell, per-month percentile threshold
    df["month"] = pd.to_datetime(df["date"]).dt.month
    thresh = (
        df.groupby(["grid_id", "month"])["rainfall_1d"]
        .transform(lambda s: np.nanpercentile(s, EXTREME_PERCENTILE))
    )
    df["is_extreme_rain"] = (df["rainfall_1d"] >= thresh).astype(int)
    df = df.drop(columns=["month"])

    return df


def run(save=True) -> pd.DataFrame:
    ds = load_rainfall_dataset()

    try:
        bbox = get_dem_bbox()
    except Exception as e:
        print(f"Warning: could not auto-detect DEM bbox ({e}); using full rainfall extent.")
        bbox = None

    df = compute_rainfall_features(ds, bbox=bbox)

    if save:
        df.to_parquet(RAINFALL_FEATURES_PARQUET, index=False)
        print(f"Saved {len(df):,} rows -> {RAINFALL_FEATURES_PARQUET}")

    return df


if __name__ == "__main__":
    run()
