"""Create optional Parquet and real Zarr examples from observations.csv.
Run inside your workshop environment after installing optional dependencies:
  pip install pyarrow zarr xarray
"""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"
df = pd.read_csv(DATA / "observations.csv")
df.to_parquet(DATA / "observations.parquet", index=False)

# Optional xarray/zarr export
import xarray as xr
indexed = df.assign(time=pd.to_datetime(df["phenomenonTime"])).set_index("time")
ds = xr.Dataset({
    "temperature_C": ("time", indexed["temperature_C"].values),
    "relative_humidity_pct": ("time", indexed["relative_humidity_pct"].values),
    "precipitation_mm": ("time", indexed["precipitation_mm"].values),
}, coords={"time": indexed.index})
ds.to_zarr(DATA / "observations_real.zarr", mode="w")
print("Created observations.parquet and observations_real.zarr")
