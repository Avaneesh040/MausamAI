# WeatherGPT feature pipeline

Turns your raw `Dataset/` folder (DEM, Gridded Rainfall, Soil, Flood history)
into one model-ready table, joined on a common 0.25-degree grid.

## Setup

```bash
pip install -r requirements.txt
```

Edit `DATASET_ROOT` at the top of `config.py` to point at your local
`Dataset` folder, then sanity-check paths:

```bash
python config.py
```

This should print all four folder paths as `exists=True` and show the DEM
bounding box it auto-detected from your tile names (currently ~N17-N18,
E081-E087 based on the tiles you've downloaded).

## One manual step before running everything

Your flood spreadsheets' actual columns aren't confirmed yet. Run:

```bash
python flood_labels.py --inspect
```

This prints the real column names and a few sample rows for all four flood
files. Open `flood_labels.py`, update `COLUMN_MAP` to match, then continue.

## Run order

You can run each module standalone (useful while debugging one data source
at a time), or run everything at once:

```bash
python rainfall_features.py   # -> pipeline_output/rainfall_features.parquet
python dem_features.py        # -> pipeline_output/dem_features.parquet
python soil_features.py       # -> pipeline_output/soil_features.parquet
python flood_labels.py        # -> pipeline_output/flood_labels.parquet

python build_master_dataset.py
# -> pipeline_output/master_table/  (parquet, partitioned by year)
```

Once you've run a module successfully once, you can skip re-running it on
subsequent builds:

```bash
python build_master_dataset.py --skip-dem --skip-soil
```

## Output schema (master_table)

| column | source | meaning |
|---|---|---|
| `grid_id` | all | stable `"{lat}_{lon}"` key for the 0.25° cell |
| `lat`, `lon` | rainfall | cell center coordinates |
| `date` | rainfall | calendar date |
| `year` | derived | partition column |
| `rainfall_1d` | rainfall | that day's rainfall (mm) |
| `rainfall_3d`, `rainfall_7d`, `rainfall_30d` | rainfall | rolling accumulations |
| `max_intensity_7d` | rainfall | peak single-day rainfall in trailing 7 days |
| `rainy_days_30d` | rainfall | count of wet days (≥2.5mm) in trailing 30 days |
| `wet_spell_length` | rainfall | consecutive wet days up to this date |
| `rainfall_anomaly_z` | rainfall | z-score vs. that cell's own monthly climatology |
| `is_extreme_rain` | rainfall | 1 if ≥95th percentile for that cell/month |
| `elevation_mean`, `elevation_min` | DEM | terrain elevation (m) |
| `slope_deg_mean`, `slope_deg_max` | DEM | slope steepness |
| `flow_accumulation_max` | DEM | *(only if richdem installed)* upstream contributing cells |
| `twi_mean` | DEM | *(only if richdem installed)* topographic wetness index |
| `soil_value`, `soil_mean_3x3`, `soil_std_3x3`, `soil_min_3x3`, `soil_max_3x3` | soil | raw soil-property features |
| `soil_local_deviation`, `soil_local_range` | soil | derived local contrast features |
| `flood_label` | flood | 1 if a documented flood event occurred at this grid_id/date, else 0 |

Terrain and soil columns are **static** — the same value repeats across every
date for a given `grid_id`, joined in at merge time.

## Known gaps to close next

1. **District-level flood records aren't joined to `grid_id` yet.**
   `District_FloodedArea` / `District_FloodImpact` / `DFSI` are district
   granularity, and joining a district polygon onto grid cells needs a
   district boundary file (shapefile/GeoJSON) you don't have in the dataset
   yet — GADM India level-2 boundaries work for this. Until then those three
   files are merged separately at district level
   (`flood_labels_district_level.parquet`) and not folded into the master
   table.

2. **Class imbalance.** Flood-positive rows will be a tiny fraction of the
   full daily grid. Don't train on the full master table as-is — either
   downsample the negative (flood_label=0) rows, or use `scale_pos_weight`
   in XGBoost / `class_weight="balanced"` in sklearn.

3. **richdem is optional.** If it's not installed, `flow_accumulation` and
   `twi` columns won't exist. Slope alone is still a reasonably strong
   terrain feature for a first model, but installing richdem is worth doing
   before your final run.

4. **LULC stays excluded**, per your PDF-map-only status — revisit once you
   have classified rasters instead of map/PDF outputs.

5. Rows with no DEM match (grid cells outside your current tile coverage,
   which is currently only ~N17-N18/E081-E087) will have NaN terrain
   columns — `build_master_dataset.py` warns about this count; drop those
   rows before training rather than imputing them.
