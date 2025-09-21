import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# INPUTS
# -----------------------------
HOURLY_MATCH_CSV = "hourly_pv_load_match.csv"
OUTPUT_BATTERY_CSV = "battery_storage_sim.csv"

BATTERY_EFFICIENCY = 0.90   # round-trip efficiency
DEPTH_OF_DISCHARGE = 0.80   # usable fraction
# Optional: initial battery size guess (kWh)
BATTERY_CAPACITY_KWH = 50

# -----------------------------
# SCRIPT
# -----------------------------
# 1) load hourly PV vs load
df = pd.read_csv(HOURLY_MATCH_CSV, parse_dates=["timestamp"])
df = df.sort_values("timestamp").reset_index(drop=True)

# 2) battery simulation
n_hours = len(df)
soc = np.zeros(n_hours)   # state of charge
battery_capacity = BATTERY_CAPACITY_KWH
battery_used = np.zeros(n_hours)
unmet_load = np.zeros(n_hours)

for i in range(n_hours):
    pv_surplus = df.loc[i, "surplus"]   # kW available to charge
    load_deficit = df.loc[i, "deficit"] # kW needed to cover

    # charge battery with surplus PV
    charge_possible = pv_surplus * BATTERY_EFFICIENCY
    soc[i] = soc[i-1] + charge_possible if i > 0 else charge_possible
    # limit by battery capacity * DoD
    soc[i] = min(soc[i], battery_capacity)

    # discharge to cover deficit
    if load_deficit > 0:
        if soc[i] > 0:
            discharge = min(soc[i], load_deficit / BATTERY_EFFICIENCY)
            soc[i] -= discharge
            battery_used[i] = discharge * BATTERY_EFFICIENCY
            unmet_load[i] = max(load_deficit - battery_used[i], 0)
        else:
            battery_used[i] = 0
            unmet_load[i] = load_deficit
    else:
        battery_used[i] = 0
        unmet_load[i] = 0

# 3) add results to dataframe
df["soc_kwh"] = soc
df["battery_used_kwh"] = battery_used
df["unmet_load_kwh"] = unmet_load
df["total_load_supplied"] = df["on_site_use"] + df["battery_used_kwh"]

# 4) metrics
annual_load = df["load_kw"].sum()
total_on_site = df["on_site_use"].sum()
total_battery = df["battery_used_kwh"].sum()
self_consumption = (total_on_site + total_battery) / df["pv_kw"].sum()
self_sufficiency = (total_on_site + total_battery) / annual_load

print("\n📊 Battery & Storage Simulation Metrics:")
print(f"Battery capacity used: {battery_capacity} kWh")
print(f"Total energy supplied by battery: {total_battery:.2f} kWh")
print(f"Unmet load (kWh): {df['unmet_load_kwh'].sum():.2f} kWh")
print(f"Self-consumption with battery: {self_consumption*100:.1f}%")
print(f"Self-sufficiency with battery: {self_sufficiency*100:.1f}%")

# 5) save hourly battery simulation
df.to_csv(OUTPUT_BATTERY_CSV, index=False)
print(f"\nSaved hourly battery simulation to: {OUTPUT_BATTERY_CSV}")

# 6) plot sample month
month = 1  # January
df_month = df[df["timestamp"].dt.month == month].set_index("timestamp")
plt.figure(figsize=(12,5))
plt.plot(df_month.index, df_month["load_kw"], label="Load (kW)")
plt.plot(df_month.index, df_month["pv_kw"], label="PV (kW)")
plt.plot(df_month.index, df_month["total_load_supplied"], label="Supplied load (PV + battery)")
plt.plot(df_month.index, df_month["soc_kwh"], label="Battery SOC (kWh)")
plt.fill_between(df_month.index, 0, df_month["battery_used_kwh"], color="orange", alpha=0.3, label="Battery discharge")
plt.title("Hourly Load, PV, and Battery — January")
plt.xlabel("Time")
plt.ylabel("kW / kWh")
plt.legend()
plt.tight_layout()
plt.show()
