# generate_hourly_load.py
import pandas as pd
import numpy as np
import calendar

# -----------------------------
# INPUTS
# -----------------------------
METEO_CSV = "site_meteo_hourly.csv"
OUTPUT_HOURLY = "estate_hourly_load.csv"

monthly_estate_load_kwh = {
    1: 1568.72,
    2: 1245.40,
    3: 1580.15,
    4: 1437.22,
    5: 1407.59,
    6: 1088.94,
    7: 1052.02,
    8: 1156.03,
    9: 1137.89,
    10: 1297.18,
    11: 1272.94,
    12: 1640.10
}

daily_shape = np.array([
    0.03, 0.025, 0.02, 0.02, 0.03, 0.05,
    0.07, 0.06, 0.05, 0.04, 0.035, 0.03,
    0.03, 0.03, 0.035, 0.04, 0.05, 0.08,
    0.12, 0.13, 0.08, 0.05, 0.04, 0.03
], dtype=float)

def main():
    # ✅ FIXED: read file & parse timestamp correctly
    df_m = pd.read_csv(METEO_CSV)
    df_m["timestamp"] = pd.to_datetime(df_m["timestamp"], format="%Y%m%d:%H%M")

    df_m = df_m.sort_values("timestamp").reset_index(drop=True)
    timestamps = df_m["timestamp"].copy()

    df_out = pd.DataFrame({"timestamp": timestamps})
    df_out["date"] = df_out["timestamp"].dt.date
    df_out["month"] = df_out["timestamp"].dt.month

    daily_frac = daily_shape / daily_shape.sum()

    load_values = []
    for date, group in df_out.groupby("date"):
        month = pd.to_datetime(date).month
        days_in_month = calendar.monthrange(date.year, month)[1]
        monthly_target = monthly_estate_load_kwh.get(month)
        daily_target = monthly_target / days_in_month

        hours = group["timestamp"].dt.hour.values
        hour_fracs = np.array([daily_frac[h] for h in hours])
        hour_fracs = hour_fracs / hour_fracs.sum()
        hourly_kwh = daily_target * hour_fracs
        load_values.extend(hourly_kwh.tolist())

    df_out["load_kw"] = load_values
    df_out["hour_kwh"] = df_out["load_kw"]

    monthly_sum = df_out.groupby("month")["hour_kwh"].sum()
    annual_sum = monthly_sum.sum()

    print("\nGenerated hourly load profile summary:")
    print(monthly_sum.round(2))
    print(f"\nAnnual load total (kWh): {annual_sum:.2f}")
    print(f"Expected annual total (kWh): {sum(monthly_estate_load_kwh.values()):.2f}")

    df_out[["timestamp", "load_kw"]].to_csv(OUTPUT_HOURLY, index=False)
    print(f"\nSaved hourly load profile to: {OUTPUT_HOURLY}")

if __name__ == "__main__":
    main()
