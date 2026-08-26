import argparse
from pathlib import Path

import pandas as pd

from config import FLOOD_DIR, FLOOD_LABELS_PARQUET


FLOOD_DIR = Path(FLOOD_DIR)
FLOOD_LABELS_PARQUET = Path(FLOOD_LABELS_PARQUET)

FLOOD_FILES = {
    "dfsi": "DFSI.csv",
    "district_flooded_area": "District_FloodedArea.csv",
    "district_flood_impact": "District_FloodImpact.csv",
    "inventory": "India_Flood_Inventory_v3.csv",
}


COLUMN_MAP = {
    "inventory": {
        "date": "Start Date",
        "district": "Districts",
        "state": "State",
        "lat": "Latitude",
        "lon": "Longitude",
    },
    "district_flooded_area": {
        "district": "Dist_Name",
        "flooded_area": "Percent_Flooded_Area",
    },
    "district_flood_impact": {
        "district": "Dist_Name",
        "impact": "Population",
    },
}


def get_path(key):
    path = FLOOD_DIR / FLOOD_FILES[key]

    if not path.exists():
        raise FileNotFoundError(
            f"\nFlood file not found:\n{path}"
        )

    return path


def inspect_files():

    for key, filename in FLOOD_FILES.items():

        path = get_path(key)

        try:
            df = pd.read_csv(path, nrows=5)

            print()
            print("=" * 70)
            print(filename)
            print("=" * 70)
            print("Columns:")
            print(list(df.columns))
            print()
            print(df.head().to_string())

        except Exception as e:
            print(
                f"[ERROR] Could not read {path}: {e}"
            )


def load_point_inventory():

    path = get_path("inventory")
    cfg = COLUMN_MAP["inventory"]

    print()
    print("Loading flood inventory:")
    print(path)

    df = pd.read_csv(path)

    df.columns = df.columns.str.strip()

    print(f"Loaded {len(df):,} flood events")

    required = [
        cfg["date"],
        cfg["district"],
        cfg["state"],
    ]

    missing = [
        c for c in required
        if c not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing inventory columns: {missing}\n"
            f"Available columns: {list(df.columns)}"
        )

    df["date"] = pd.to_datetime(
        df[cfg["date"]],
        errors="coerce",
        dayfirst=True
    )

    valid_dates = df["date"].notna()

    print(
        f"Valid dates: "
        f"{valid_dates.sum():,} / {len(df):,}"
    )

    df["year"] = df["date"].dt.year

    df["district"] = (
        df[cfg["district"]]
        .astype(str)
        .str.strip()
    )

    df["state"] = (
        df[cfg["state"]]
        .astype(str)
        .str.strip()
    )

    df["flood"] = 1

    has_coordinates = (
        cfg["lat"] in df.columns
        and cfg["lon"] in df.columns
    )

    if has_coordinates:

        lat = pd.to_numeric(
            df[cfg["lat"]],
            errors="coerce"
        )

        lon = pd.to_numeric(
            df[cfg["lon"]],
            errors="coerce"
        )

        valid_coordinates = (
            lat.notna()
            & lon.notna()
            & lat.between(-90, 90)
            & lon.between(-180, 180)
        )

        print(
            f"Valid coordinates: "
            f"{valid_coordinates.sum():,} / {len(df):,}"
        )

    else:

        valid_coordinates = pd.Series(
            False,
            index=df.index
        )

        print(
            "Latitude/Longitude columns not available."
        )

    coordinate_count = valid_coordinates.sum()

    if coordinate_count > 0:

        print(
            "Coordinate-based flood mapping available."
        )

        from grid_utils import (
            make_grid_id,
            snap_to_grid
        )

        lat = lat.loc[valid_coordinates]
        lon = lon.loc[valid_coordinates]

        lat_grid, lon_grid = snap_to_grid(
            lat,
            lon
        )

        point_df = df.loc[
            valid_coordinates
        ].copy()

        point_df["grid_id"] = make_grid_id(
            lat_grid,
            lon_grid
        )

        result = point_df[
            [
                "grid_id",
                "date",
                "year",
                "district",
                "state",
                "flood",
            ]
        ].dropna(
            subset=["date"]
        )

        print(
            f"Created {len(result):,} "
            "point-level flood labels"
        )

        print(
            f"Grid cells containing flood events: "
            f"{result['grid_id'].nunique():,}"
        )

        return result

    print()
    print(
        "WARNING: Inventory contains no usable "
        "Latitude/Longitude values."
    )

    print(
        "Keeping flood events at district level "
        "instead of discarding them."
    )

    result = df[
        [
            "date",
            "year",
            "district",
            "state",
            "flood",
        ]
    ].dropna(
        subset=["date"]
    )

    print(
        f"Created {len(result):,} "
        "district-level inventory events"
    )

    return result


def load_district_flooded_area():

    path = get_path(
        "district_flooded_area"
    )

    cfg = COLUMN_MAP[
        "district_flooded_area"
    ]

    df = pd.read_csv(path)

    df.columns = df.columns.str.strip()

    required = [
        cfg["district"],
        cfg["flooded_area"],
    ]

    missing = [
        c for c in required
        if c not in df.columns
    ]

    if missing:
        raise ValueError(
            "Missing columns in "
            f"District_FloodedArea.csv: {missing}"
        )

    result = df[
        required
    ].copy()

    result = result.rename(
        columns={
            cfg["district"]: "district",
            cfg["flooded_area"]: "flooded_area",
        }
    )

    result["district"] = (
        result["district"]
        .astype(str)
        .str.strip()
    )

    result["flooded_area"] = pd.to_numeric(
        result["flooded_area"],
        errors="coerce"
    )

    return result


def load_district_flood_impact():

    path = get_path(
        "district_flood_impact"
    )

    cfg = COLUMN_MAP[
        "district_flood_impact"
    ]

    df = pd.read_csv(path)

    df.columns = df.columns.str.strip()

    required = [
        cfg["district"],
        cfg["impact"],
    ]

    missing = [
        c for c in required
        if c not in df.columns
    ]

    if missing:
        raise ValueError(
            "Missing columns in "
            f"District_FloodImpact.csv: {missing}"
        )

    result = df[
        required
    ].copy()

    result = result.rename(
        columns={
            cfg["district"]: "district",
            cfg["impact"]: "population_affected",
        }
    )

    result["district"] = (
        result["district"]
        .astype(str)
        .str.strip()
    )

    result["population_affected"] = pd.to_numeric(
        result["population_affected"],
        errors="coerce"
    )

    return result


def merge_district_labels():

    area = load_district_flooded_area()

    impact = load_district_flood_impact()

    area = (
        area
        .groupby("district", as_index=False)
        .agg({
            "flooded_area": "mean"
        })
    )

    impact = (
        impact
        .groupby("district", as_index=False)
        .agg({
            "population_affected": "mean"
        })
    )

    out = area.merge(
        impact,
        on="district",
        how="outer"
    )

    out["flood"] = 1

    print()
    print(
        f"District-level flood records: "
        f"{len(out):,}"
    )

    return out


def save_inventory_labels(
    inventory,
    output_path
):

    inventory.to_parquet(
        output_path,
        index=False
    )

    print()
    print(
        f"Saved {len(inventory):,} "
        f"inventory flood records -> "
        f"{output_path}"
    )


def run(save=True):

    print()
    print("=" * 70)
    print("FLOOD LABEL GENERATION")
    print("=" * 70)

    inventory = load_point_inventory()

    if save:

        inventory_output = (
            FLOOD_LABELS_PARQUET
        )

        save_inventory_labels(
            inventory,
            inventory_output
        )

    district_labels = (
        merge_district_labels()
    )

    if not district_labels.empty:

        district_output = (
            FLOOD_LABELS_PARQUET.parent
            / "flood_labels_district_level.parquet"
        )

        district_labels.to_parquet(
            district_output,
            index=False
        )

        print(
            f"Saved {len(district_labels):,} "
            f"district-level rows -> "
            f"{district_output}"
        )

    print()
    print("=" * 70)
    print("FLOOD LABEL GENERATION COMPLETE")
    print("=" * 70)

    return inventory


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--inspect",
        action="store_true",
        help="Print flood file columns and sample rows"
    )

    args = parser.parse_args()

    if args.inspect:
        inspect_files()
    else:
        run()