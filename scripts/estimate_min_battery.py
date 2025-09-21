import pandas as pd
import numpy as np

# -----------------------------
# INPUTS
# -----------------------------
HOURLY_MATCH_CSV = "hourly_pv_load_match.csv"  # hourly PV vs load results
BATTERY_EFFICIENCY = 0.90   # round-trip efficiency
DEPTH_OF_DISCHARGE = 0.80   # usable fraction

# battery search range (kWh) — using list instead of np.arange to avoid PyCharm warnings
battery_sizes = list(range(10, 201, 10))  # 10 kWh → 200 kWh in steps of 10

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv(HOURLY_MATCH_CSV, parse_dates=["timestamp"])
df = df.sort_values("timestamp").reset_index(drop=True)

# -----------------------------
# BATTERY SIMULATION FUNCTION
# -----------------------------
def simulate_battery(capacity_kwh: float) -> float:
    """
    Simulates battery operation for a given capacity (kWh)
    Returns total unmet load (kWh) for the year
    """
    n_hours = len(df)
    soc = np.zeros(n_hours)  # state of charge
    unmet_load = np.zeros(n_hours)

    for i in range(n_hours):
        pv_surplus = df.loc[i, "surplus"]
        load_deficit = df.loc[i, "deficit"]

        # Charge battery with PV surplus
        charge_possible = pv_surplus * BATTERY_EFFICIENCY
        soc[i] = soc[i - 1] + charge_possible if i > 0 else charge_possible
        soc[i] = min(soc[i], capacity_kwh)

        # Discharge to cover deficit
        if load_deficit > 0:
            if soc[i] > 0:
                discharge = min(soc[i], load_deficit / BATTERY_EFFICIENCY)
                soc[i] -= discharge
                unmet_load[i] = max(load_deficit - discharge * BATTERY_EFFICIENCY, 0)
            else:
                unmet_load[i] = load_deficit
        else:
            unmet_load[i] = 0

    return float(unmet_load.sum())

# -----------------------------
# SEARCH FOR MINIMUM BATTERY
# -----------------------------
min_capacity = None
for size in battery_sizes:
    unmet = simulate_battery(size)
    print(f"Battery {size} kWh → Unmet load: {unmet:.2f} kWh")
    if unmet <= 1:  # negligible unmet load
        min_capacity = size
        break

# -----------------------------
# RESULTS
# -----------------------------
if min_capacity:
    print(f"\n✅ Minimum battery capacity to cover all deficits: {min_capacity} kWh")
else:
    print("\n⚠️ Even 200 kWh not enough to cover all deficits. Consider larger battery or hybrid solution.")
