import pandas as pd
from pulp import LpProblem, LpVariable, LpBinary, LpMinimize, lpSum
from sklearn.preprocessing import MinMaxScaler


bus_df = pd.read_csv("../노선_요약.csv")
subway_df = pd.read_csv("../지하철_요약.csv")
cafe_df = pd.read_csv("../일반음식점(카페)현황.csv", encoding = 'CP949')
park_df = pd.read_csv("../도시공원정보현황(제공표준).csv", encoding = 'CP949')
trash_bin_df = pd.read_csv("../경기도 성남시_쓰레기통_설치현황_20250325.csv")

# 데이터 필터링 및 정제
cafe_df = cafe_df[(cafe_df['시군명'] == '성남시') & (cafe_df['영업상태명'] == '영업')]
cafe_df = cafe_df.rename(columns = {'WGS84위도': '위도', 'WGS84경도': '경도', '사업장명': '이름'})
park_df = park_df[park_df['소재지지번주소'].str.startswith('경기도 성남시')]
park_df = park_df.dropna(subset=['위도', '경도'])
park_df = park_df.rename(columns = {'공원명': '이름'})
subway_df = subway_df.rename(columns = {'역사명': '이름'})
bus_df = bus_df.dropna().rename(columns = {'정류장명': '이름'})

# 가중치 계산
scaler = MinMaxScaler()
cafe_df['가중치'] = scaler.fit_transform(cafe_df[['총시설규모(㎡)']])
park_df['가중치'] = scaler.fit_transform(park_df[['공원면적(㎡)']])
bus_df['혼잡도'] = bus_df['환승시간(분)'] * bus_df['노선개수']
bus_df['가중치'] = scaler.fit_transform(bus_df[['혼잡도']])
subway_df['일평균승하차인원'] = subway_df['승차총승객수'] + subway_df['하차총승객수']
subway_df['가중치'] = scaler.fit_transform(subway_df[['일평균승하차인원']])


demand_df = pd.concat([
    cafe_df[['위도', '경도', '이름', '가중치']],
    park_df[['위도', '경도', '이름', '가중치']],
    subway_df[['위도', '경도', '이름', '가중치']],
    bus_df[['위도', '경도', '이름', '가중치']]
], ignore_index=True)

demand_points = list(zip(demand_df['위도'], demand_df['경도'], demand_df['가중치'], demand_df['이름']))

candidate_df = trash_bin_df.dropna(subset=['위도', '경도'])
candidate_bins = list(zip(candidate_df['위도'], candidate_df['경도'], candidate_df['설치위치']))



from geopy.distance import geodesic

distance_matrix = [
    [geodesic(dp[:2], cb[:2]).meters for cb in candidate_bins]
    for dp in demand_points
]

num_demands = len(demand_points)
num_candidates = len(candidate_bins)
p = 100  # 개수 제한


x = [LpVariable(f"x_{j}", cat=LpBinary) for j in range(num_candidates)]
assign = [[LpVariable(f"assign_{i}_{j}", cat=LpBinary) for j in range(num_candidates)] for i in range(num_demands)]
z = LpVariable("z", lowBound=0, cat="Continuous") 

model = LpProblem("P_Center_Problem", LpMinimize)
model += z  

for i in range(num_demands):
    model += lpSum(assign[i][j] for j in range(num_candidates)) == 1
    for j in range(num_candidates):
        model += assign[i][j] <= x[j]
    model += lpSum(distance_matrix[i][j] * assign[i][j] for j in range(num_candidates)) <= z 

model += lpSum(x) <= p

model.solve()

selected_locations = []
for j in range(num_candidates):
    if x[j].varValue > 0.5:
        lat, lon, name = candidate_bins[j]
        selected_locations.append((lat, lon, name))

print(f"\n[설치된 위치 개수: {len(selected_locations)}개 | 최대 커버 거리: {z.varValue:.2f}m]")
for loc in selected_locations[:10]: 
    print(f"설치 위치: {loc[2]} @ ({loc[0]:.5f}, {loc[1]:.5f})")
