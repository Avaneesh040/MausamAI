"""
config.py
---------
Central configuration for the WeatherGPT flood/rainfall feature pipeline.

Edit DATASET_ROOT to point at your local "Dataset" folder. Everything else
is derived automatically (grid resolution from the rainfall files, bounding
box from the DEM tile names) so you don't have to hardcode coordinates by hand.
"""

import re
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. Point this at your Dataset folder
# ---------------------------------------------------------------------------
DATASET_ROOT = Path(r"C:\Users\KIIT\Desktop\WeatherGPT\Dataset")  # <-- EDIT ME

RAINFALL_DIR = DATASET_ROOT / "Gridded Rainfall (0.25 x 0.25)"
DEM_DIR = DATASET_ROOT / "DEM"
SOIL_DIR = DATASET_ROOT / "Soil"
FLOOD_DIR = DATASET_ROOT / "Flood history"

# ---------------------------------------------------------------------------
# 2. Output locations
# ---------------------------------------------------------------------------
OUTPUT_DIR = Path(r"C:\Users\KIIT\Desktop\WeatherGPT\preprocessing\pipeline_output")
OUTPUT_DIR.mkdir(exist_ok=True)

RAINFALL_FEATURES_PARQUET = OUTPUT_DIR / "rainfall_features.parquet"
DEM_FEATURES_PARQUET = OUTPUT_DIR / "dem_features.parquet"
SOIL_FEATURES_PARQUET = OUTPUT_DIR / "soil_features.parquet"
FLOOD_LABELS_PARQUET = OUTPUT_DIR / "flood_labels.parquet"
MASTER_TABLE_DIR = OUTPUT_DIR / "master_table"  # written as partitioned parquet

# ---------------------------------------------------------------------------
# 3. Grid + feature parameters
# ---------------------------------------------------------------------------
GRID_RESOLUTION_DEG = 0.25          # matches IMD RF25 rainfall grid
WET_DAY_THRESHOLD_MM = 2.5          # IMD's standard "rainy day" threshold
EXTREME_PERCENTILE = 95             # per-cell, per-month percentile for "extreme rain"
ROLLING_WINDOWS_DAYS = [1, 3, 7, 30]

# ---------------------------------------------------------------------------
# 4. Auto-detect DEM bounding box from tile folder names
# ---------------------------------------------------------------------------
_TILE_NAME_RE = re.compile(r"N(\d{2})_00_E(\d{3})_00")


def get_dem_bbox(dem_dir: Path = DEM_DIR):
    """
    Copernicus DEM tiles are named like Copernicus_DSM_COG_10_N17_00_E082_00_DEM,
    where N17/E082 is the tile's SOUTH-WEST corner and each tile is 1 degree
    square. Scanning the folder names gives you the exact bbox you have DEM
    coverage for, so rainfall/soil can be clipped to match instead of pulling
    all of India.

    Returns (lat_min, lat_max, lon_min, lon_max).
    """
    if not dem_dir.exists():
        raise FileNotFoundError(f"DEM directory not found: {dem_dir}")

    lats, lons = [], []
    for tile_dir in dem_dir.iterdir():
        if not tile_dir.is_dir():
            continue
        m = _TILE_NAME_RE.search(tile_dir.name)
        if m:
            lat_sw, lon_sw = int(m.group(1)), int(m.group(2))
            lats.extend([lat_sw, lat_sw + 1])
            lons.extend([lon_sw, lon_sw + 1])

    if not lats:
        raise ValueError(
            f"No tiles matching the Copernicus naming pattern found in {dem_dir}. "
            "Check DEM_DIR in config.py."
        )

    return min(lats), max(lats), min(lons), max(lons)


if __name__ == "__main__":
    # Quick sanity check: run `python config.py` to confirm paths resolve
    # and the DEM bbox looks right before running the rest of the pipeline.
    print("DATASET_ROOT :", DATASET_ROOT, "exists:", DATASET_ROOT.exists())
    for name, p in [
        ("RAINFALL_DIR", RAINFALL_DIR),
        ("DEM_DIR", DEM_DIR),
        ("SOIL_DIR", SOIL_DIR),
        ("FLOOD_DIR", FLOOD_DIR),
    ]:
        print(f"{name:15s}: {p}  exists={p.exists()}")

    try:
        bbox = get_dem_bbox()
        print(f"\nDetected DEM bbox -> lat [{bbox[0]}, {bbox[1]}], lon [{bbox[2]}, {bbox[3]}]")
    except Exception as e:
        print(f"\nCould not detect DEM bbox yet: {e}")
