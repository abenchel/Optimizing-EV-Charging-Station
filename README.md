# 🚀 Optimizing EV Charging Station Placement using K-Medians & Interactive Visualization

## 📌 Project Overview

This project focuses on **optimizing the placement of electric vehicle (EV) charging stations** using the **K-Medians clustering algorithm**. By leveraging **spatial data analysis** and **interactive visualization**, we aim to strategically position charging stations to **enhance accessibility, efficiency, and demand coverage**.

## 🏆 Key Features

- 📊 **Data Collection & Preprocessing** – Aggregating geospatial, traffic, and demographic data.
- 📌 **K-Medians Clustering** – Identifying optimal charging station locations based on real-world data.
- 🗺️ **Interactive Visualization** – Using Folium and Plotly for mapping and analytics.
- ⚡ **Scalable & Robust Model** – Designed for urban planning and mobility optimization.

---

## 🛠️ Technologies & Libraries

This project is implemented using:

- **Python**
- **Scikit-learn** – K-Medians clustering
- **Pandas & NumPy** – Data processing
- **Folium & Plotly** – Interactive visualization
- **Geopandas** – Spatial data handling

---

## 📈 Methodology

### 1️⃣ Data Collection & Cleaning
   - Gathered geospatial data (EV stations, road networks, population density).  
   - Cleaned and normalized datasets for consistency.

### 2️⃣ K-Medians Clustering
   - Applied K-Medians instead of K-Means for **outlier-resistant clustering**.  
   - Used Manhattan distance for more **realistic urban mobility modeling**.

### 3️⃣ Visualization & Evaluation
   - Plotted station locations using **Folium interactive maps**.  
   - Evaluated results based on coverage, accessibility, and cost-efficiency.

---

## 📊 Results & Insights

✔️ **Optimized station locations** improve accessibility & efficiency.  
✔️ **Interactive visualization** enables better decision-making.  
✔️ **K-Medians** proves to be more robust than K-Means for this application.

---

🚀 Getting Started

📥 Download Data

The required dataset can be downloaded from Kaggle: https://www.kaggle.com/code/jocelyndumlao/ev-distribution-traits-analysis/input' . Make sure to place the dataset in folder before running the project.


📌 Installation

Clone the repository:

```bash
https://github.com/abenchel/Optimizing-EV-Charging-Station.git
cd Optimizing-EV-Charging-Station
```


Install dependencies:
```bash
pip install -r requirements.txt
```

🏃 Run the Project

To execute clustering and visualize results:

```bash
python k-medians.py
```

After running the script, a small window will appear where you need to choose a value for k (the number of charging stations). Once selected, a .html file will be generated in the project folder. Open this file using Live Server to visualize the optimized charging station locations interactively.

🎯 Future Improvements

🔄 Real-time station demand updates using dynamic datasets.

🏙 Expansion to other urban infrastructure like parking spaces & public transport hubs.

🧠 Integration with AI models for predictive analytics.

👥 Contributors

Benchelha Ayoub

Ouhammou Brahim
