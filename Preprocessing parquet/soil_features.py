import pandas as pd
from pathlib import Path

from config import SOIL_DIR, SOIL_FEATURES_PARQUET
from grid_utils import make_grid_id, snap_to_grid

SOIL_VALUE_COLS = [
    "soil_value",
    "soil_mean_3x3",
    "soil_std_3x3",
    "soil_min_3x3",
    "soil_max_3x3",
]

CHUNK_SIZE = 500_000


def _sniff_real_format(path):
    with open(path, "rb") as f:
        head = f.read(8)

    if head[:2] == b"PK":
        return "xlsx"

    if head[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":
        return "xls"

    return "text"


def find_soil_file(soil_dir=SOIL_DIR, filename="soil_ml_ready"):
    matches = list(Path(soil_dir).glob(f"{filename}.*"))

    if not matches:
        raise FileNotFoundError(
            f"No file named {filename}.* found in {soil_dir}"
        )

    return matches[0]


def validate_columns(columns):
    required = ["latitude", "longitude"] + SOIL_VALUE_COLS

    missing = [c for c in required if c not in columns]

    if missing:
        raise ValueError(
            f"Missing columns: {missing}\n"
            f"Available columns: {list(columns)}"
        )


def process_chunk(df):
    validate_columns(df.columns)

    before = len(df)

    all_zero = (df[SOIL_VALUE_COLS] == 0).all(axis=1)

    df = df.loc[~all_zero, [
        "latitude",
        "longitude",
        *SOIL_VALUE_COLS
    ]].copy()

    dropped = before - len(df)

    if len(df) == 0:
        return None, dropped

    lat_grid, lon_grid = snap_to_grid(
        df["latitude"],
        df["longitude"]
    )

    df["grid_id"] = make_grid_id(
        lat_grid,
        lon_grid
    )

    df["soil_local_deviation"] = (
        df["soil_value"] -
        df["soil_mean_3x3"]
    )

    df["soil_local_range"] = (
        df["soil_max_3x3"] -
        df["soil_min_3x3"]
    )

    agg_cols = SOIL_VALUE_COLS + [
        "soil_local_deviation",
        "soil_local_range"
    ]

    sums = df.groupby("grid_id")[agg_cols].sum()

    counts = df.groupby("grid_id")[agg_cols].count()

    return (sums, counts), dropped


def run(save=True):
    path = find_soil_file()

    fmt = _sniff_real_format(path)

    print(f"Detected soil file: {path}")
    print(f"Detected format: {fmt}")
    print(f"Chunk size: {CHUNK_SIZE:,}")
    print()

    if fmt != "text":
        raise RuntimeError(
            "This memory-efficient version expects the soil_ml_ready "
            "file to be CSV/TSV text. Your current file was detected "
            f"as {fmt}."
        )

    totals = {}
    counts = {}

    total_rows = 0
    total_dropped = 0
    chunk_number = 0

    print("Starting chunked soil processing...")

    reader = pd.read_csv(
        path,
        sep=",",
        chunksize=CHUNK_SIZE,
        low_memory=True
    )

    for chunk in reader:
        chunk_number += 1

        rows = len(chunk)
        total_rows += rows

        result, dropped = process_chunk(chunk)

        total_dropped += dropped

        if result is not None:
            sums, chunk_counts = result

            for grid_id in sums.index:

                if grid_id not in totals:
                    totals[grid_id] = sums.loc[grid_id].copy()
                    counts[grid_id] = chunk_counts.loc[grid_id].copy()
                else:
                    totals[grid_id] += sums.loc[grid_id]
                    counts[grid_id] += chunk_counts.loc[grid_id]

        print(
            f"[Chunk {chunk_number}] "
            f"Rows: {rows:,} | "
            f"Nodata removed: {dropped:,} | "
            f"Total processed: {total_rows:,}"
        )

        del chunk

    print()
    print("Finished reading soil data.")
    print(f"Total rows: {total_rows:,}")
    print(f"Total nodata rows removed: {total_dropped:,}")

    if not totals:
        raise RuntimeError(
            "No valid soil data remained after removing nodata rows."
        )

    print("Building final grid-level soil dataset...")

    grid_ids = list(totals.keys())

    rows = []

    for grid_id in grid_ids:

        row = {"grid_id": grid_id}

        for col in SOIL_VALUE_COLS + [
            "soil_local_deviation",
            "soil_local_range"
        ]:
            count = counts[grid_id][col]

            if count > 0:
                row[col] = (
                    totals[grid_id][col] /
                    count
                )
            else:
                row[col] = float("nan")

        rows.append(row)

    grid_df = pd.DataFrame(rows)

    print(f"Final grid cells: {len(grid_df):,}")

    if save:
        grid_df.to_parquet(
            SOIL_FEATURES_PARQUET,
            index=False
        )

        print(
            f"Saved {len(grid_df):,} grid cells -> "
            f"{SOIL_FEATURES_PARQUET}"
        )

    return grid_df


if __name__ == "__main__":
    run()