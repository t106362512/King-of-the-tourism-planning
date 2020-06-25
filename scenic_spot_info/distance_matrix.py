# radarsearch.py
import googlemaps
import os
import json
from datetime import datetime

# from google_maps_services_python_master.tests.test_distance_matrix import DistanceMatrixTest

GOOGLE_PLACES_API_KEY = 'AIzaSyCcnZRtkbHg4X80RTTQSz60a2SvqmBitp8'

# Client
gmaps = googlemaps.Client(key=GOOGLE_PLACES_API_KEY)

# this origins from mo
origins = [[121.60546, 25.28247],
           [121.84354, 25.10815],
           [121.52081, 25.19156],
           [121.55292, 25.27472],
           [121.43855, 25.17181],
           [121.42752, 25.10372],
           [121.54404, 25.29054],
           [121.50055, 25.06498],
           [121.44421, 24.97271],
           [121.53531, 25.29261]]

for i in range(len(origins)):
    origins[i] = [origins[i][1], origins[i][0]]

destinations = [[121.60546, 25.28247],
                [121.84354, 25.10815],
                [121.52081, 25.19156],
                [121.55292, 25.27472],
                [121.43855, 25.17181],
                [121.42752, 25.10372],
                [121.54404, 25.29054],
                [121.50055, 25.06498],
                [121.44421, 24.97271],
                [121.53531, 25.29261]]
                
for i in range(len(destinations)):
    destinations[i] = [destinations[i][1], destinations[i][0]]


# Name = 北海高爾夫球場, Local = [121.60546, 25.28247]
# Name = 翁山英故居(九份茶坊), Local = [121.84354, 25.10815]
# Name = 反經石, Local = [121.52081, 25.19156]
# Name = 聖明宮千年雀榕, Local = [121.55292, 25.27472]
# Name = 滬尾馬偕醫館, Local = [121.43855, 25.17181]
# Name = 旗竿湖教育農場, Local = [121.42752, 25.10372]
# Name = 小梅街道, Local = [121.54404, 25.29054]
# Name = 三和夜市, Local = [121.50055, 25.06498]
# Name = 土城廣承岩寺, Local = [121.44421, 24.97271]
# Name = 富基漁港, Local = [121.53531, 25.29261]


now = datetime.now()
matrix = gmaps.distance_matrix(
    origins,
    destinations,
    mode="driving",
    language="zh-TW",
    units="metric",
    departure_time=now
)

with open('test.json', 'w', encoding='UTF-8') as fo:
    json.dump(matrix, fo, indent=4, ensure_ascii=False)

print(matrix)

# Radar search
# location = (25.017156, 121.506359)
# radius = 25000
# place_type = 'restaurant'
# places_radar_result = gmaps.places_radar(location, radius, type=place_type)

# print(places_radar_result)
