import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import haversine_distances

trashcan_path = "경기도 성남시_쓰레기통_설치현황_20250325.csv"
bus_path = "노선_요약.csv"
subway_path = "지하철_요약.csv"

EARTH_RADIUS = 6371000
RADIUS_COVER = 1000      # coverage radius
RADIUS_CONGESTION = 1000 # congestion radius

trash_df = pd.read_csv(trashcan_path).dropna(subset=["위도", "경도"])
bus_df = pd.read_csv(bus_path).dropna(subset=["위도", "경도"])
subway_df = pd.read_csv(subway_path).dropna(subset=["위도", "경도"])

# 위경도 → 라디안 변환
trash_coords = np.radians(trash_df[["위도", "경도"]].values)
bus_coords = np.radians(bus_df[["위도", "경도"]].values)
subway_coords = np.radians(subway_df[["위도", "경도"]].values)

# 거리 계산
bus_dists = haversine_distances(trash_coords, bus_coords) * EARTH_RADIUS
subway_dists = haversine_distances(trash_coords, subway_coords) * EARTH_RADIUS

# 성능 평가
results = []
for i in range(trash_coords.shape[0]):
    trash_lat, trash_lng = trash_df.iloc[i][["위도", "경도"]]

    covered_bus_indices = np.where(bus_dists[i] <= RADIUS_COVER)[0]
    covered_subway_indices = np.where(subway_dists[i] <= RADIUS_COVER)[0]

    distances = np.concatenate([bus_dists[i][covered_bus_indices], subway_dists[i][covered_subway_indices]])
    if len(distances) == 0:
        avg_dist = np.nan
        max_dist = np.nan
        eff_score = 0
    else:
        avg_dist = np.mean(distances)
        max_dist = np.max(distances)
        eff_score = (len(distances) / avg_dist) if avg_dist > 0 else 0

    self_coord = trash_coords[i].reshape(1, -1)
    all_dists = haversine_distances(self_coord, trash_coords) * EARTH_RADIUS
    congestion = np.sum((all_dists[0] <= RADIUS_CONGESTION) & (all_dists[0] > 0))

    results.append({
        "id": i,
        "latitude": round(trash_lat, 6),
        "longitude": round(trash_lng, 6),
        "covered_bus": len(covered_bus_indices),
        "covered_subway": len(covered_subway_indices),
        "total_coverage": len(distances),
        "avg_distance_m": round(avg_dist, 2) if not np.isnan(avg_dist) else None,
        "max_distance_m": round(max_dist, 2) if not np.isnan(max_dist) else None,
        "efficiency_score": round(eff_score, 4),
        "congestion_1000m": int(congestion)
    })


df_result = pd.DataFrame(results)
df_result.to_csv("trashcan_performance_metrics_1000.csv", index=False)
print("Saved")
