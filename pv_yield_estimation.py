import pandas as pd
import pvlib
import matplotlib.pyplot as plt

# --- System Parameters ---
system_size_kw = 10        # PV system size in kWp
tilt = 10                  # Panel tilt angle (deg) ~ site latitude
azimuth = 180              # South-facing (180° in Northern Hemisphere)
performance_ratio = 0.75   # Accounts for system losses

# --- Load Monthly GHI ---
monthly_ghi = pd.read_csv("monthly_ghi.csv", index_col=0)
monthly_ghi.index = monthly_ghi.index.astype(int)  # Ensure month is integer

print("📊 Monthly GHI [kWh/m²]:")
print(monthly_ghi)

# --- PV Yield Estimation ---
# Simplified model: PV energy = GHI × system_size × PR
# Assume PV efficiency is already wrapped into PR
monthly_yield = monthly_ghi["ghi"] * system_size_kw * performance_ratio

# Add to dataframe
results = pd.DataFrame({
    "GHI (kWh/m²)": monthly_ghi["ghi"],
    "PV Yield (kWh)": monthly_yield
})

# --- Yearly totals ---
yearly_ghi = monthly_ghi["ghi"].sum()
yearly_yield = monthly_yield.sum()

print("\n🌞 Yearly GHI [kWh/m²]:", yearly_ghi)
print("⚡ Yearly PV Yield [kWh] for", system_size_kw, "kWp system:", yearly_yield)

# --- Save Results ---
results.to_csv("pv_yield_results.csv")
print("\n✅ Results saved to pv_yield_results.csv")

# --- Plot PV Yield ---
results["PV Yield (kWh)"].plot(kind="bar", color="green", edgecolor="black")
plt.title(f"Estimated Monthly PV Yield ({system_size_kw} kWp)")
plt.xlabel("Month")
plt.ylabel("Energy [kWh]")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
