import pandas as pd
import matplotlib.pyplot as plt

# ---- SETTINGS ----
INPUT_CSV = "site_meteo_hourly.csv"   # your meteo CSV

# ---- STEP 1: Load and inspect ----
df = pd.read_csv(INPUT_CSV)

print("CSV columns detected:", df.columns.tolist())
print("\nFirst 5 rows of raw data:")
print(df.head(5))
print("\nData types before cleaning:")
print(df.dtypes)

# ---- STEP 2: Parse timestamp ----
df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    format="%Y%m%d:%H%M",   # adjust if your timestamps are different
    errors="coerce"
)

df = df.dropna(subset=["timestamp"])   # drop bad/missing timestamps

# ---- STEP 3: Ensure numeric columns ----
num_cols = ["ghi", "dni", "dhi", "amb_temp_c", "wind_speed_m_s", "relative_humidity"]

for col in num_cols:
    if col in df.columns:
        print(f"Cleaning column: {col}")
        # Force string -> strip spaces -> numeric
        df[col] = pd.to_numeric(df[col].astype(str).str.strip(), errors="coerce")

print("\nData after cleaning (first 5 rows):")
print(df[num_cols].head(5))
print("\nData types after cleaning:")
print(df[num_cols].dtypes)

# Drop rows where GHI is missing
df = df.dropna(subset=["ghi"])

# ---- STEP 4: Add month column ----
df = df.sort_values("timestamp")
df["month"] = df["timestamp"].dt.month

# ---- STEP 5: Calculate monthly solar resource ----
monthly_ghi = df.groupby("month")["ghi"].sum() / 1000  # convert Wh/m² -> kWh/m²

print("\n🌞 Monthly Global Horizontal Irradiance (GHI) [kWh/m²]:")
print(monthly_ghi)

# ---- STEP 6: Plot results ----
if not monthly_ghi.empty:
    plt.figure(figsize=(8, 5))
    monthly_ghi.plot(kind="bar", color="orange", edgecolor="black")
    plt.ylabel("GHI (kWh/m²)")
    plt.xlabel("Month")
    plt.title("Monthly Solar Resource")
    plt.grid(True, axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()
else:
    print("⚠️ No GHI data found to plot.")

monthly_ghi.to_csv("monthly_ghi.csv")

