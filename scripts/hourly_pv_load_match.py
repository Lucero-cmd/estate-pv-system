import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# INPUTS
# -----------------------------
HOURLY_LOAD_CSV = "estate_hourly_load.csv"
METEO_CSV = "site_meteo_hourly.csv"
OUTPUT_MATCH_CSV = "hourly_pv_load_match.csv"

SYSTEM_KWP = 10        # PV system size
PR = 0.75              # performance ratio

# -----------------------------
# SCRIPT
# -----------------------------
# 1) load files
df_load = pd.read_csv(HOURLY_LOAD_CSV, parse_dates=["timestamp"])
df_meteo = pd.read_csv(METEO_CSV)
df_meteo["timestamp"] = pd.to_datetime(df_meteo["timestamp"], format="%Y%m%d:%H%M")

# merge on timestamp
df = pd.merge(df_load, df_meteo[["timestamp", "ghi"]], on="timestamp", how="left")

# 2) compute hourly PV production (kW)
# GHI in W/m2 → kW/m2: divide by 1000
df["pv_kw"] = df["ghi"] / 1000 * SYSTEM_KWP * PR

# 3) compute on-site use, surplus, deficit
df["on_site_use"] = np.minimum(df["load_kw"], df["pv_kw"])
df["surplus"] = np.maximum(df["pv_kw"] - df["load_kw"], 0)
df["deficit"] = np.maximum(df["load_kw"] - df["pv_kw"], 0)

# 4) monthly and annual metrics
df["month"] = df["timestamp"].dt.month
monthly = df.groupby("month").agg({
    "pv_kw": "sum",
    "load_kw": "sum",
    "on_site_use": "sum",
    "surplus": "sum",
    "deficit": "sum"
}).rename(columns={
    "pv_kw": "pv_kwh",
    "load_kw": "load_kwh",
    "on_site_use": "on_site_use_kwh",
    "surplus": "surplus_kwh",
    "deficit": "deficit_kwh"
})

annual = monthly.sum()
self_consumption = annual["on_site_use_kwh"] / annual["pv_kwh"]
self_sufficiency = annual["on_site_use_kwh"] / annual["load_kwh"]

print("\n✅ Monthly summary (kWh):")
print(monthly.round(1))
print("\n📊 Annual summary (kWh):")
print(annual.round(1))
print(f"\n⚡ Self-consumption: {self_consumption*100:.1f}%")
print(f"🔋 Self-sufficiency: {self_sufficiency*100:.1f}%")

# 5) save hourly match
df[["timestamp", "pv_kw", "load_kw", "on_site_use", "surplus", "deficit"]].to_csv(OUTPUT_MATCH_CSV, index=False)
print(f"\nSaved hourly PV-load match to: {OUTPUT_MATCH_CSV}")

# 6) plot sample month (e.g., January)
jan = df[df["month"] == 1].set_index("timestamp")
plt.figure(figsize=(12,5))
plt.plot(jan.index, jan["load_kw"], label="Load (kW)")
plt.plot(jan.index, jan["pv_kw"], label="PV production (kW)")
plt.fill_between(jan.index, jan["on_site_use"], color="green", alpha=0.3, label="On-site PV use")
plt.title("Hourly PV vs Load — January")
plt.xlabel("Time")
plt.ylabel("kW")
plt.legend()
plt.tight_layout()
plt.show()
