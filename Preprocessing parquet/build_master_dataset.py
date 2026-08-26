"""
build_master_dataset.py
-----------------------

Builds the final master flood-risk dataset by combining:

1. Rainfall features
   - grid_id + date

2. DEM features
   - grid_id only

3. Soil features
   - grid_id only

4. Flood inventory
   - district + date

5. District → grid spatial mapping
   - district → grid_id
   - overlap_fraction

The district flood events are converted into grid-level flood labels
using district_grid_mapping.parquet.

Final structure:

    grid_id + date
            |
            +-- rainfall
            +-- DEM
            +-- soil
            +-- flood label

Output:
    MASTER_TABLE_DIR
"""

import argparse
from pathlib import Path

import pandas as pd

import dem_features
import flood_labels
import rainfall_features
import soil_features

from config import (
    DEM_FEATURES_PARQUET,
    FLOOD_LABELS_PARQUET,
    MASTER_TABLE_DIR,
    RAINFALL_FEATURES_PARQUET,
    SOIL_FEATURES_PARQUET,
)


# -------------------------------------------------------------------
# DISTRICT → GRID MAPPING
# -------------------------------------------------------------------

DISTRICT_GRID_MAPPING = (
    Path(r"C:\Users\KIIT\Desktop\WeatherGPT\preprocessing\pipeline_output")
    / "district_grid_mapping.parquet"
)


# -------------------------------------------------------------------
# NORMALIZE DISTRICT / STATE NAMES
# -------------------------------------------------------------------

def normalize_key(series):
    """
    Normalizes district/state names so that flood inventory names
    can match the district boundary mapping.
    """

    return (
        series
        .astype(str)
        .str.upper()
        .str.strip()
        .str.replace("&", "AND", regex=False)
        .str.replace(r"[^A-Z0-9]", "", regex=True)
    )


# -------------------------------------------------------------------
# CREATE GRID-LEVEL FLOOD LABELS
# -------------------------------------------------------------------

def create_grid_flood_labels(flood_df, mapping):
    """
    Converts district-level flood events into grid-level flood events.

    flood_df:
        date
        year
        district
        state
        flood

    mapping:
        grid_id
        district
        state
        district_key
        state_key
        overlap_fraction

    A flood event is transferred to every grid cell that intersects
    the corresponding district.

    overlap_fraction is retained so we can later filter weak
    spatial overlaps if required.
    """

    print("\nCreating grid-level flood labels...")

    flood = flood_df.copy()
    mapping = mapping.copy()

    # ---------------------------------------------------------------
    # Normalize names
    # ---------------------------------------------------------------

    flood["district_key"] = normalize_key(
        flood["district"]
    )

    flood["state_key"] = normalize_key(
        flood["state"]
    )

    mapping["district_key"] = normalize_key(
        mapping["district_key"]
    )

    mapping["state_key"] = normalize_key(
        mapping["state_key"]
    )

    # ---------------------------------------------------------------
    # Make sure dates are datetime
    # ---------------------------------------------------------------

    flood["date"] = pd.to_datetime(
        flood["date"],
        errors="coerce"
    )

    flood = flood.dropna(subset=["date"])

    # ---------------------------------------------------------------
    # Remove duplicate flood events
    # ---------------------------------------------------------------

    flood = flood[
        [
            "date",
            "year",
            "district_key",
            "state_key",
            "flood",
        ]
    ].drop_duplicates()

    print(
        f"Flood events available: {len(flood):,}"
    )

    # ---------------------------------------------------------------
    # Keep only required mapping columns
    # ---------------------------------------------------------------

    mapping = mapping[
        [
            "grid_id",
            "district_key",
            "state_key",
            "overlap_fraction",
        ]
    ].copy()

    # ---------------------------------------------------------------
    # Remove extremely tiny spatial overlaps
    #
    # 0.01 = 1% of the grid cell
    #
    # We keep them initially because you can tune this later.
    # ---------------------------------------------------------------

    mapping = mapping[
        mapping["overlap_fraction"] > 0
    ].copy()

    print(
        f"District-grid mapping rows: {len(mapping):,}"
    )

    # ---------------------------------------------------------------
    # JOIN FLOOD EVENTS → DISTRICT → GRID
    # ---------------------------------------------------------------

    grid_flood = flood.merge(
        mapping,
        on=[
            "district_key",
            "state_key",
        ],
        how="inner",
    )

    print(
        f"Grid-level flood records after spatial mapping: "
        f"{len(grid_flood):,}"
    )

    # ---------------------------------------------------------------
    # Check whether anything matched
    # ---------------------------------------------------------------

    if grid_flood.empty:

        print(
            "\nWARNING: No flood events matched the "
            "district-grid mapping."
        )

        print("\nExample flood keys:")
        print(
            flood[
                ["district_key", "state_key"]
            ].drop_duplicates().head(10)
        )

        print("\nExample mapping keys:")
        print(
            mapping[
                ["district_key", "state_key"]
            ].drop_duplicates().head(10)
        )

        raise RuntimeError(
            "Flood districts could not be matched to "
            "district_grid_mapping.parquet."
        )

    # ---------------------------------------------------------------
    # Remove unnecessary columns
    # ---------------------------------------------------------------

    grid_flood = grid_flood[
        [
            "grid_id",
            "date",
            "year",
            "flood",
            "overlap_fraction",
        ]
    ]

    # ---------------------------------------------------------------
    # If multiple district polygons map to the same grid/date,
    # retain the strongest overlap.
    # ---------------------------------------------------------------

    grid_flood = (
        grid_flood
        .groupby(
            [
                "grid_id",
                "date",
                "year",
            ],
            as_index=False
        )
        .agg(
            flood=("flood", "max"),
            overlap_fraction=("overlap_fraction", "max"),
        )
    )

    print(
        f"Unique grid/date flood labels: "
        f"{len(grid_flood):,}"
    )

    print(
        f"Grid cells containing flood events: "
        f"{grid_flood['grid_id'].nunique():,}"
    )

    print(
        f"Flood dates represented: "
        f"{grid_flood['date'].nunique():,}"
    )

    return grid_flood


# -------------------------------------------------------------------
# BUILD MASTER DATASET
# -------------------------------------------------------------------

def build(
    skip_rainfall=False,
    skip_dem=False,
    skip_soil=False,
    skip_flood=False,
):

    print("\n")
    print("=" * 70)
    print("BUILDING MASTER DATASET")
    print("=" * 70)

    # ===============================================================
    # RAINFALL
    # ===============================================================

    if (
        skip_rainfall
        and RAINFALL_FEATURES_PARQUET.exists()
    ):

        print("\nLoading existing rainfall features...")

        rainfall_df = pd.read_parquet(
            RAINFALL_FEATURES_PARQUET
        )

    else:

        print("\nGenerating rainfall features...")

        rainfall_df = rainfall_features.run()
    rainfall_df["date"] = pd.to_datetime(
    rainfall_df["date"],
    errors="coerce"
)
    # ===============================================================
    # DEM
    # ===============================================================

    if (
        skip_dem
        and DEM_FEATURES_PARQUET.exists()
    ):

        print("\nLoading existing DEM features...")

        dem_df = pd.read_parquet(
            DEM_FEATURES_PARQUET
        )

    else:

        print("\nGenerating DEM features...")

        dem_df = dem_features.run()

    # ===============================================================
    # SOIL
    # ===============================================================

    if (
        skip_soil
        and SOIL_FEATURES_PARQUET.exists()
    ):

        print("\nLoading existing soil features...")

        soil_df = pd.read_parquet(
            SOIL_FEATURES_PARQUET
        )

    else:

        print("\nGenerating soil features...")

        soil_df = soil_features.run()

    # ===============================================================
    # FLOOD
    # ===============================================================

    if (
        skip_flood
        and FLOOD_LABELS_PARQUET.exists()
    ):

        print("\nLoading existing flood labels...")

        flood_df = pd.read_parquet(
            FLOOD_LABELS_PARQUET
        )

    else:

        print("\nGenerating flood labels...")

        flood_df = flood_labels.run()

    # ===============================================================
    # LOAD DISTRICT → GRID MAPPING
    # ===============================================================

    if not DISTRICT_GRID_MAPPING.exists():

        raise FileNotFoundError(
            "\nDistrict-grid mapping not found:\n"
            f"{DISTRICT_GRID_MAPPING}\n\n"
            "Run district_grid_mapping.py first."
        )

    print(
        "\nLoading district-grid mapping..."
    )

    mapping = pd.read_parquet(
        DISTRICT_GRID_MAPPING
    )

    print(
        f"Mapping rows: {len(mapping):,}"
    )

    print(
        f"Mapped grid cells: "
        f"{mapping['grid_id'].nunique():,}"
    )

    # ===============================================================
    # CREATE GRID-LEVEL FLOOD LABELS
    # ===============================================================

    grid_flood_df = create_grid_flood_labels(
    flood_df,
    mapping,
         )

    # Ensure both sides of the final merge use the same date dtype
    rainfall_df["date"] = pd.to_datetime(
    rainfall_df["date"],
    errors="coerce"
    )

    grid_flood_df["date"] = pd.to_datetime(
    grid_flood_df["date"],
    errors="coerce"
)

    # ===============================================================
    # BASIC INFORMATION
    # ===============================================================

    print("\n")
    print("=" * 70)
    print("INPUT DATA SUMMARY")
    print("=" * 70)

    print(
        f"Rainfall: "
        f"{len(rainfall_df):,} rows | "
        f"{rainfall_df['grid_id'].nunique():,} grids"
    )

    print(
        f"DEM: "
        f"{len(dem_df):,} grids"
    )

    print(
        f"Soil: "
        f"{len(soil_df):,} grids"
    )

    print(
        f"Flood grid labels: "
        f"{len(grid_flood_df):,}"
    )

    # ===============================================================
    # MERGE RAINFALL + DEM
    # ===============================================================

    print("\nMerging rainfall + DEM...")

    master = rainfall_df.merge(
        dem_df,
        on="grid_id",
        how="left",
    )

    print(
        f"After DEM merge: "
        f"{len(master):,} rows"
    )

    # ===============================================================
    # MERGE SOIL
    # ===============================================================

    print("\nMerging soil...")

    master = master.merge(
        soil_df,
        on="grid_id",
        how="left",
    )

    print(
        f"After soil merge: "
        f"{len(master):,} rows"
    )

    # ===============================================================
    # MERGE FLOOD LABELS
    # ===============================================================

    print("\nMerging flood labels...")

    master = master.merge(
        grid_flood_df[
            [
                "grid_id",
                "date",
                "flood",
                "overlap_fraction",
            ]
        ],
        on=[
            "grid_id",
            "date",
        ],
        how="left",
    )

    # ===============================================================
    # FILL NON-FLOOD DAYS
    # ===============================================================

    master["flood"] = (
        master["flood"]
        .fillna(0)
        .astype("int8")
    )

    master["flood_overlap_fraction"] = (
        master["overlap_fraction"]
        .fillna(0)
    )

    master.drop(
        columns=["overlap_fraction"],
        inplace=True,
    )

    # ===============================================================
    # DATE
    # ===============================================================

    master["date"] = pd.to_datetime(
        master["date"],
        errors="coerce",
    )

    master["year"] = (
        master["date"]
        .dt.year
        .astype("Int16")
    )

    # ===============================================================
    # MISSING DATA CHECK
    # ===============================================================

    print("\nChecking missing DEM features...")

    if "slope_deg_mean" in master.columns:

        n_missing = (
            master["slope_deg_mean"]
            .isna()
            .sum()
        )

        print(
            f"Rows missing DEM: "
            f"{n_missing:,}"
        )

    print("\nChecking missing soil features...")

    if "soil_value" in master.columns:

        n_missing = (
            master["soil_value"]
            .isna()
            .sum()
        )

        print(
            f"Rows missing soil: "
            f"{n_missing:,}"
        )

    # ===============================================================
    # SAVE
    # ===============================================================

    MASTER_TABLE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("\nSaving master dataset...")

    master.to_parquet(
        MASTER_TABLE_DIR,
        partition_cols=["year"],
        index=False,
    )

    # ===============================================================
    # FINAL SUMMARY
    # ===============================================================

    print("\n")
    print("=" * 70)
    print("MASTER DATASET COMPLETE")
    print("=" * 70)

    print(
        f"Rows: {len(master):,}"
    )

    print(
        f"Columns: {len(master.columns):,}"
    )

    print(
        f"Grid cells: "
        f"{master['grid_id'].nunique():,}"
    )

    print(
        f"Dates: "
        f"{master['date'].nunique():,}"
    )

    positive = master["flood"].sum()

    print(
        f"Positive flood labels: "
        f"{positive:,}"
    )

    print(
        f"Flood prevalence: "
        f"{100 * master['flood'].mean():.3f}%"
    )

    print(
        f"\nSaved to:\n{MASTER_TABLE_DIR}"
    )

    return master


# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--skip-rainfall",
        action="store_true",
    )

    parser.add_argument(
        "--skip-dem",
        action="store_true",
    )

    parser.add_argument(
        "--skip-soil",
        action="store_true",
    )

    parser.add_argument(
        "--skip-flood",
        action="store_true",
    )

    args = parser.parse_args()

    build(
        skip_rainfall=args.skip_rainfall,
        skip_dem=args.skip_dem,
        skip_soil=args.skip_soil,
        skip_flood=args.skip_flood,
    )