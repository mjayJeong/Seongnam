# 2025 Seongnam Public Data Analysis Contest

## 📌 Project Overview

This project aims to identify optimal locations for installing public trash bins in Seongnam City through spatial analysis using public data. By incorporating factors such as floating population, waste generation, and lifestyle zones, the goal is to develop a data-driven strategy that balances **urban aesthetics** and **policy efficiency**.

---

## 🧩 Data Sources

| Dataset Name                                   | Source                                                                 |
|------------------------------------------------|------------------------------------------------------------------------|
| Trash bin installation status in Seongnam      | [data.go.kr](https://www.data.go.kr)                                   |
| Bus stops in Seongnam                          | [data.go.kr](https://www.data.go.kr)                                   |
| Public transit transfer times                  | [Gyeonggi Transport Center](https://gits.gg.go.kr)                     |
| Number of routes per stop                      | [Gyeonggi Transport Center](https://gits.gg.go.kr)                     |
| Subway station boarding/alighting data         | [Seoul Open Data Plaza](https://data.seoul.go.kr)                      |
| Subway station info                            | [Seoul Open Data Plaza](https://data.seoul.go.kr)                      |
| Urban park information                         | [Gyeonggi Data Dream](https://data.gg.go.kr)                           |
| Café locations and size                        | [Gyeonggi Data Dream](https://data.gg.go.kr)                           |
| Waste processing volume by district            | [Seongnam Data Net](https://data.seongnam.go.kr)                       |
| Floating population statistics                 | [Gyeonggi Data Analysis Portal](https://insight.gg.go.kr)              |

---


## 🛠 Tech Stack

- **Programming & Analysis**: Python (Pandas, Numpy, SKlearn, PuLP)
- **Visualization**: Folium, QGIS, React

---

## 📈 Methodology Summary
```
MCLP (Maximum Coverage Location Problem): Finds the best p locations to **maximize demand coverage** within a fixed radius.
K-means Clustering: Groups dense demand points and places bins at **cluster centers**.
Greedy MCLP: Quickly selects locations by **iteratively adding the most effective** candidate.
Ensemble: Combines all three methods to choose **overlapping results for higher stability**.
```

---

## 📊 Visualization Result
| ![Map2](https://github.com/user-attachments/assets/773698ac-83aa-4f4e-a847-6b92f5429134) | ![Map3](https://github.com/user-attachments/assets/adb134ed-4758-4f5f-88c8-3fb3f64b98f1) |
|------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| *Final Candidate Sites: Sujeong-gu*                                                     | *Final Candidate Sites: Jungwon-gu*                                                       |

| ![Map4](https://github.com/user-attachments/assets/2e36d3aa-c077-48c0-8252-3d906f0e2b24) | ![Map1](https://github.com/user-attachments/assets/953916f0-4295-431e-914f-2c36f101a585)  |
|------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| *Final Candidate Sites: Bundang-gu*                                                     | *Final Candidate Sites: Pangyo*                                                           |
