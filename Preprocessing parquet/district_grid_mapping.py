from pathlib import Path
import re

import pandas as pd
import geopandas as gpd
from shapely.geometry import box


BASE_DIR = Path(r"C:\Users\KIIT\Desktop\WeatherGPT")

BOUNDARY_FILE = (
    BASE_DIR
    / "Dataset"
    / "Boundries"
    / "gadm41_IND_2.json"
)

PIPELINE_OUTPUT = (
    BASE_DIR
    / "preprocessing"
    / "pipeline_output"
)

RAINFALL_FILE = PIPELINE_OUTPUT / "rainfall_features.parquet"

OUTPUT_FILE = PIPELINE_OUTPUT / "district_grid_mapping.parquet"

GRID_RESOLUTION = 0.25


def normalize_name(value):

    if pd.isna(value):
        return ""

    value = str(value).upper().strip()

    value = value.replace("&", "AND")
    value = value.replace("-", " ")
    value = value.replace("_", " ")

    value = re.sub(r"[^A-Z0-9 ]", " ", value)
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def load_grid():

    print("Loading rainfall grid...")

    df = pd.read_parquet(
        RAINFALL_FILE,
        columns=["grid_id"]
    )

    grid_ids = (
        df["grid_id"]
        .dropna()
        .drop_duplicates()
        .astype(str)
    )

    print(f"Unique grid cells: {len(grid_ids):,}")

    coords = grid_ids.str.split("_", expand=True)

    grid = pd.DataFrame({
        "grid_id": grid_ids.values,
        "grid_lat": pd.to_numeric(coords[0]),
        "grid_lon": pd.to_numeric(coords[1]),
    })

    return grid


def create_grid_polygons(grid):

    print("Creating 0.25-degree grid polygons...")

    half = GRID_RESOLUTION / 2

    geometry = [
        box(
            lon - half,
            lat - half,
            lon + half,
            lat + half
        )
        for lat, lon in zip(
            grid["grid_lat"],
            grid["grid_lon"]
        )
    ]

    gdf = gpd.GeoDataFrame(
        grid.copy(),
        geometry=geometry,
        crs="EPSG:4326"
    )

    return gdf


def load_districts():

    print("Loading India district boundaries...")

    if not BOUNDARY_FILE.exists():

        raise FileNotFoundError(
            f"Boundary file not found:\n{BOUNDARY_FILE}"
        )

    districts = gpd.read_file(BOUNDARY_FILE)

    print(
        f"Loaded {len(districts):,} district polygons"
    )

    print(
        "Boundary columns:",
        list(districts.columns)
    )

    return districts


def prepare_districts(districts):

    required = ["NAME_1", "NAME_2"]

    missing = [
        col
        for col in required
        if col not in districts.columns
    ]

    if missing:

        raise ValueError(
            f"Missing expected GADM columns: {missing}\n"
            f"Available columns: {list(districts.columns)}"
        )

    districts = districts[
        ["GID_2", "NAME_1", "NAME_2", "geometry"]
    ].copy()

    districts = districts.rename(
        columns={
            "GID_2": "gid_2",
            "NAME_1": "state",
            "NAME_2": "district"
        }
    )

    districts["state_key"] = (
        districts["state"]
        .apply(normalize_name)
    )

    districts["district_key"] = (
        districts["district"]
        .apply(normalize_name)
    )

    districts = districts.to_crs("EPSG:4326")

    districts["geometry"] = (
        districts.geometry
        .make_valid()
    )

    return districts

def build_mapping(grid, districts):

    print("Finding grid/district intersections...")

    joined = gpd.sjoin(
        grid,
        districts,
        how="inner",
        predicate="intersects"
    )

    print(f"Initial intersections: {len(joined):,}")

    if joined.empty:
        raise RuntimeError(
            "No grid cells intersected district boundaries."
        )

    grid_metric = (
        grid[["grid_id", "geometry"]]
        .copy()
        .to_crs("EPSG:6933")
    )

    district_metric = (
        districts[
            [
                "gid_2",
                "state",
                "district",
                "state_key",
                "district_key",
                "geometry"
            ]
        ]
        .copy()
        .to_crs("EPSG:6933")
    )

    pairs = gpd.sjoin(
        grid_metric,
        district_metric,
        how="inner",
        predicate="intersects"
    )

    print("Calculating overlap fractions...")

    rows = []

    for grid_id, group in pairs.groupby("grid_id"):

        grid_geom = (
            grid_metric[
                grid_metric["grid_id"] == grid_id
            ]
            .geometry
            .iloc[0]
        )

        grid_area = grid_geom.area

        for _, row in group.iterrows():

            district_idx = row["index_right"]

            district_geom = district_metric.loc[
                district_idx,
                "geometry"
            ]

            district_area = district_geom.area

            intersection_area = (
                grid_geom
                .intersection(district_geom)
                .area
            )

            if grid_area > 0:
                overlap_fraction = (
                    intersection_area / grid_area
                )
            else:
                overlap_fraction = 0.0

            if district_area > 0:
                district_fraction = (
                    intersection_area / district_area
                )
            else:
                district_fraction = 0.0

            if overlap_fraction > 0:

                rows.append({
                    "grid_id": grid_id,
                    "gid_2": row["gid_2"],
                    "state": row["state"],
                    "district": row["district"],
                    "state_key": row["state_key"],
                    "district_key": row["district_key"],
                    "overlap_fraction": overlap_fraction,
                    "district_fraction": district_fraction,
                    "intersection_area": intersection_area,
                    "grid_area": grid_area,
                    "district_area": district_area
                })

    mapping = pd.DataFrame(rows)

    return mapping


def add_grid_coordinates(mapping, grid):

    mapping = mapping.merge(
        grid[
            [
                "grid_id",
                "grid_lat",
                "grid_lon"
            ]
        ],
        on="grid_id",
        how="left"
    )

    cols = [
        "grid_id",
        "grid_lat",
        "grid_lon",
        "gid_2",
        "state",
        "district",
        "state_key",
        "district_key",
        "overlap_fraction",
        "district_fraction",
        "intersection_area",
        "grid_area",
        "district_area"
    ]

    return mapping[cols]
def validate_mapping(mapping, grid):

    print()
    print("=" * 70)
    print("MAPPING VALIDATION")
    print("=" * 70)

    print(
        f"Grid cells available: "
        f"{len(grid):,}"
    )

    print(
        f"Grid cells mapped: "
        f"{mapping['grid_id'].nunique():,}"
    )

    print(
        f"Grid cells without district: "
        f"{len(grid) - mapping['grid_id'].nunique():,}"
    )

    print(
        f"Districts represented: "
        f"{mapping['district'].nunique():,}"
    )

    print(
        f"Mapping rows: "
        f"{len(mapping):,}"
    )

    print()
    print("Sample:")

    print(
        mapping
        .sort_values(
            ["grid_id", "overlap_fraction"],
            ascending=[True, False]
        )
        .head(15)
        .to_string(index=False)
    )

    print()

    print("Overlap fraction statistics:")

    print(
        mapping["overlap_fraction"]
        .describe()
    )


def main():

    print()
    print("=" * 70)
    print("DISTRICT → GRID MAPPING")
    print("=" * 70)

    grid = load_grid()

    grid_gdf = create_grid_polygons(
        grid
    )

    districts = load_districts()

    districts = prepare_districts(
        districts
    )

    mapping = build_mapping(
        grid_gdf,
        districts
    )

    mapping = add_grid_coordinates(
        mapping,
        grid
    )

    validate_mapping(
        mapping,
        grid
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    mapping.to_parquet(
        OUTPUT_FILE,
        index=False
    )

    print()
    print(
        f"Saved {len(mapping):,} mapping rows ->"
    )

    print(OUTPUT_FILE)

    print()
    print("DISTRICT → GRID MAPPING COMPLETE")


if __name__ == "__main__":
    main()