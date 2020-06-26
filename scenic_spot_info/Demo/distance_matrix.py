# radarsearch.py
from TravelGraph import TSP
from pprint import pprint
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

org = list(map(lambda x: (x[1],x[0]), origins))

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
                
dest = list(map(lambda x: (x[1],x[0]), destinations))

now = datetime.now()
matrix = gmaps.distance_matrix(
    org,
    dest,
    mode="driving",
    language="zh-TW",
    units="metric",
    departure_time=now
)

with open('test.json', 'w', encoding='UTF-8') as fo:
    json.dump(matrix, fo, indent=4, ensure_ascii=False)

r = TSP().from_gmaps_matrix(matrix, map_list=origins).normal_ans()
pprint(r)
# print(matrix)