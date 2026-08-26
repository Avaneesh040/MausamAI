"""
dem_features.py
----------------
Processes Copernicus DEM tiles one at a time, derives terrain variables,
and aggregates them onto the 0.25-degree rainfall grid.

Requires: rasterio, numpy, pandas.
richdem is optional.

Run standalone:
    python dem_features.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
import rasterio

from config import DEM_DIR, DEM_FEATURES_PARQUET, GRID_RESOLUTION_DEG
from grid_utils import make_grid_id

try:
    import richdem as rd
    HAVE_RICHDEM = True
except ImportError:
    HAVE_RICHDEM = False


DOWNSAMPLE_FACTOR = 12


def find_dem_tiles(dem_dir: Path = DEM_DIR):
    tiles = []

    for tile_dir in sorted(dem_dir.iterdir()):
        if not tile_dir.is_dir():
            continue

        candidates = list(tile_dir.glob("*DEM*.tif"))
        candidates = [
            c for c in candidates
            if c.parent == tile_dir
        ]

        if not candidates:
            candidates = list(tile_dir.glob("*.tif"))
            candidates = [
                c for c in candidates
                if c.parent == tile_dir
            ]

        if candidates:
            tiles.append(candidates[0])

    if not tiles:
        raise FileNotFoundError(
            f"No DEM .tif files found in {dem_dir}"
        )

    print(f"Found {len(tiles)} DEM tiles.")
    return tiles


def read_dem_tile(tile_path):
    with rasterio.open(tile_path) as src:

        out_height = max(1, src.height // DOWNSAMPLE_FACTOR)
        out_width = max(1, src.width // DOWNSAMPLE_FACTOR)

        elevation = src.read(
            1,
            out_shape=(out_height, out_width),
            resampling=rasterio.enums.Resampling.bilinear
        ).astype("float32")

        transform = src.transform * src.transform.scale(
            src.width / out_width,
            src.height / out_height
        )

        nodata = src.nodata

        if nodata is not None:
            elevation[elevation == nodata] = np.nan

        elevation[elevation < -1000] = np.nan

        return elevation, transform, src.crs


def compute_terrain_rasters(elevation, transform):
    rows, cols = elevation.shape

    lat_center = (
        transform.f
        + (rows / 2) * transform.e
    )

    lat_rad = np.radians(abs(lat_center))

    pixel_y_m = abs(transform.e) * 111320
    pixel_x_m = abs(transform.a) * 111320 * np.cos(lat_rad)

    pixel_x_m = max(pixel_x_m, 1.0)
    pixel_y_m = max(pixel_y_m, 1.0)

    safe_elevation = np.where(
        np.isfinite(elevation),
        elevation,
        np.nan
    )

    dzdy, dzdx = np.gradient(
        safe_elevation,
        pixel_y_m,
        pixel_x_m
    )

    slope_rad = np.arctan(
        np.sqrt(
            dzdx ** 2 +
            dzdy ** 2
        )
    )

    slope_deg = np.degrees(slope_rad)

    rasters = {
        "elevation": elevation,
        "slope_deg": slope_deg
    }

    if HAVE_RICHDEM:

        rd_elev = rd.rdarray(
            np.where(
                np.isfinite(elevation),
                elevation,
                -9999
            ),
            no_data=-9999
        )

        rd_elev.geotransform = transform.to_gdal()

        filled = rd.FillDepressions(
            rd_elev,
            epsilon=True,
            in_place=False
        )

        flow_acc = rd.FlowAccumulation(
            filled,
            method="D8"
        )

        flow_acc = np.array(
            flow_acc,
            dtype="float32"
        )

        rasters["flow_accumulation"] = flow_acc

        slope_rad_safe = np.where(
            slope_rad <= 0,
            1e-6,
            slope_rad
        )

        twi = np.log(
            (flow_acc + 1)
            / np.tan(slope_rad_safe)
        )

        twi[~np.isfinite(elevation)] = np.nan

        rasters["twi"] = twi

    return rasters


def aggregate_tile_to_grid(
    rasters,
    transform,
    res=GRID_RESOLUTION_DEG
):

    nrows, ncols = rasters["elevation"].shape

    row_idx, col_idx = np.indices(
        (nrows, ncols)
    )

    lon = (
        transform.c
        + (col_idx + 0.5) * transform.a
    )

    lat = (
        transform.f
        + (row_idx + 0.5) * transform.e
    )

    grid_lat, grid_lon = grid_utils_snap(
        lat,
        lon,
        res
    )

    grid_id = make_grid_id(
        grid_lat.ravel(),
        grid_lon.ravel()
    )

    data = {
        "grid_id": grid_id
    }

    for name, arr in rasters.items():
        data[name] = arr.ravel()

    df = pd.DataFrame(data)

    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    agg = {
        "elevation": [
            "mean",
            "min",
            "max"
        ],
        "slope_deg": [
            "mean",
            "max"
        ]
    }

    if "flow_accumulation" in rasters:
        agg["flow_accumulation"] = [
            "max"
        ]

    if "twi" in rasters:
        agg["twi"] = [
            "mean"
        ]

    grouped = (
        df
        .groupby("grid_id")
        .agg(agg)
    )

    grouped.columns = [
        "_".join(c)
        for c in grouped.columns
    ]

    grouped = grouped.reset_index()

    return grouped


def grid_utils_snap(lat, lon, res):

    from grid_utils import snap_to_grid

    return snap_to_grid(
        lat,
        lon,
        res
    )


def run(save=True):

    tiles = find_dem_tiles()

    tile_results = []

    total = len(tiles)

    for i, tile_path in enumerate(
        tiles,
        start=1
    ):

        print(
            f"[{i}/{total}] "
            f"Processing {tile_path.name}"
        )

        try:

            elevation, transform, crs = read_dem_tile(
                tile_path
            )

            print(
                f"    Raster shape after "
                f"downsampling: {elevation.shape}"
            )

            rasters = compute_terrain_rasters(
                elevation,
                transform
            )

            tile_df = aggregate_tile_to_grid(
                rasters,
                transform
            )

            tile_results.append(
                tile_df
            )

            del elevation
            del rasters
            del tile_df

        except Exception as e:

            print(
                f"    FAILED: {tile_path.name}"
            )

            print(
                f"    Error: {e}"
            )

    if not tile_results:
        raise RuntimeError(
            "No DEM features were generated."
        )

    print(
        "Combining tile-level results..."
    )

    df = pd.concat(
        tile_results,
        ignore_index=True
    )

    df = (
        df
        .groupby("grid_id")
        .mean(numeric_only=True)
        .reset_index()
    )

    if save:

        DEM_FEATURES_PARQUET.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        df.to_parquet(
            DEM_FEATURES_PARQUET,
            index=False
        )

        print(
            f"Saved {len(df):,} grid cells -> "
            f"{DEM_FEATURES_PARQUET}"
        )

    return df


if __name__ == "__main__":
    run()