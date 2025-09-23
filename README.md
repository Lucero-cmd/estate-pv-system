# 🌞 Estate PV System Optimization Project  

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
[![GitHub repo](https://img.shields.io/badge/GitHub-Lucero--cmd/estate--pv--system-black?logo=github)](https://github.com/Lucero-cmd/estate-pv-system)  

This repository contains the **Horizon Estate Solar PV optimization project (Lagos, Nigeria)**.  
It demonstrates **resource assessment, load estimation, PV yield modeling, and battery storage simulations** using Python and PV design tools (HelioScope & PVsyst).  

---

## 📂 Project Structure
estate-pv-system/
│── data/ # Input data (meteo, load profiles)
│── scripts/ # Python scripts (irradiance, load, battery)
│── results/ # Output CSVs, plots, reports
│── README.md # Project overview
│── .gitignore


---

## ⚡ Key Steps Completed
- ✅ **Meteo analysis** → Processed hourly irradiance & weather data  
- ✅ **Resource assessment** → Monthly & annual GHI calculated  
- ✅ **Load profile generation** → Estimated hourly demand for estate  
- ✅ **PV yield estimation** → 10 kWp system → ~13.2 MWh/year  
- ✅ **Battery simulation** → Tested 10–200 kWh storage capacity  
- ✅ **HelioScope & PVsyst design** → Layout, orientation, losses  

---

## 📊 Results
- **Annual GHI**: ~1765 kWh/m²  
- **10 kWp PV yield**: ~13.2 MWh/year  
- **Annual load**: ~15.9 MWh  
- **Battery performance**:  
  - 10 kWh battery → high unmet load (~7.5 MWh)  
  - 50 kWh battery → unmet load reduced (~4.1 MWh)  
  - ≥50 kWh → diminishing returns  


---

## 🔧 Tools & Technologies
- **Python** (pandas, numpy, matplotlib)  
- **HelioScope** → PV layout & design  
- **PVSyst** → Yield & losses modeling  
- **GitHub** → Version control  

---

## 📑 Reports
- [PVsyst Design Report (PDF)](results/Horizon_estate_project.pdf)  
- Word-format project report (in progress)  

---



---

## 👤 Author
**Osemudiamen Ozah (Lucero-cmd)**  
- GitHub: [Lucero-cmd](https://github.com/Lucero-cmd)  

- Email: osemudiamen.ozah@gmail.com  

---

## 📜 License
This project is licensed under the [MIT License](LICENSE).  
