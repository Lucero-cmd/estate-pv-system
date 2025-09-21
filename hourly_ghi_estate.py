import pandas as pd
import numpy as np

# -----------------------------
# Inputs
# -----------------------------
monthly_ghi = {
    1: 174.30220,
    2: 138.37785,
    3: 175.57230,
    4: 159.69140,
    5: 156.39910,
    6: 120.99390,
    7: 116.89025,
    8: 128.44810,
    9: 126.43160,
    10: 144.13105,
    11: 141.43780,
    12: 182.23285
}

# Average daylight hours per month in Lagos (approx)
daylight_hours = {
    1: 12, 2: 12, 3: 12, 4: 12,
    5: 12, 6: 12, 7: 12, 8: 12,
    9: 12, 10: 12, 11: 12, 12: 12
}

# -----------------------------
# Generate hourly timestamps and GHI
# -----------------------------
records = []

for month in range(1, 13):
    total_kwh = monthly_ghi[month]
    days_in_month = pd.Period(f"2022-{month:02d}").days_in_month
    daily_ghi = total_kwh / days_in_month  # kWh/day

    # distribute over daylight hours using simple sinusoidal profile
    hours = np.arange(6, 18)  # 6 AM → 5 PM daylight
    sin_profile = np.sin(np.pi * (hours - 6) / 12)  # 0 → 1 → 0
    sin_profile = sin_profile / sin_profile.sum()  # normalize

    hourly_ghi = daily_ghi * sin_profile  # kWh per hour

    for day in range(1, days_in_month + 1):
        for i, hour in enumerate(hours):
            timestamp = pd.Timestamp(f"2022-{month:02d}-{day:02d} {hour:02d}:00")
            ghi_value = hourly_ghi[i]
            records.append([timestamp, ghi_value])

# Create DataFrame
df_ghi = pd.DataFrame(records, columns=["timestamp", "ghi"])
df_ghi.to_csv("hourly_ghi_estate.csv", index=False)
print("✅ Generated hourly GHI CSV: hourly_ghi_estate.csv")
