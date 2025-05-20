import json
from collections import defaultdict
from geopy.distance import geodesic
import folium
import pandas as pd

# 오차 범위 (비슷한 좌표 같은 걸로 뭉치는 용도)
location_tolerance = 20

def load_csv(path):
    df = pd.read_csv(path, encoding='cp949')
    return df.to_dict(orient='records') 

# 파일 이름, 경로 수정 (json 파일 쓸수도 있어서 json import 해놓음)
mclp_results = load_csv("mclp_installed_bins.csv")
pmedian_results = load_csv("greedy_mclp_installed_bins.csv")
kmeans_results = load_csv("k-means_installed_bins.csv")



total_models = [mclp_results, pmedian_results, kmeans_results]
vote_counter = []

# column 이름에 맞게 수정
for model in total_models:
    for place in model:
        matched = False
        for item in vote_counter:
            dist = geodesic((place["위도"], place["경도"]), (item["위도"], item["경도"])).meters
            if dist <= location_tolerance:
                item["votes"] += 1
                item["이름들"].add(place["이름"])
                matched = True
                break
        if not matched:  
            vote_counter.append({
                "위도": place["위도"],
                "경도": place["경도"],
                "votes": 1,
                "이름들": set([place["이름"]])
            })


# 간단하게 voting 방식 사용했음 (2개 이상 투표된 것들만 추출)
final_locations = [loc for loc in vote_counter if loc["votes"] >= 2]

print(f"total count : {len(final_locations)}")


# 지도 중심
if final_locations:
    center_lat = sum([l["위도"] for l in final_locations]) / len(final_locations)
    center_lon = sum([l["경도"] for l in final_locations]) / len(final_locations)
else:
    center_lat, center_lon = 37.4, 127.1  

m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

for loc in final_locations:
    folium.Marker(
        location=[loc["위도"], loc["경도"]],
        tooltip=f"Votes: {loc['votes']} | {', '.join(loc['이름들'])}",
        icon=folium.Icon(color='green', icon='trash', prefix='fa')
    ).add_to(m)

# 결과물 html로 저장
m.save("ensemble_result.html")
# m
