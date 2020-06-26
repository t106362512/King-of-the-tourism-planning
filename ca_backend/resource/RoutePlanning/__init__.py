from datetime import datetime
from .TravelGraph import TSP
from pprint import pprint
import googlemaps
import gmplot
import json
import os

class RoutePlanning:

    def __init__(self, *args, **kwargs):

        self.google_api_key = kwargs.get('google_api_key', os.getenv('GOOGLE_PLACES_API_KEY'))
        self.gmaps = googlemaps.Client(key=self.google_api_key)

    def get_shortest(self, localtion_list:list, *args, **kwargs):

        
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

        now = datetime.now()
        org = list(map(lambda x: (x[1],x[0]), localtion_list))

        matrix = self.gmaps.distance_matrix(
            org,
            org,
            mode="driving",
            language="zh-TW",
            units="metric",
            departure_time=now
        )
        min_path_length, min_path_list = TSP().from_gmaps_matrix(matrix, map_list=org).normal_ans(start=0)

        return min_path_length, min_path_list

    def get_shortest_map(self, localtion_list:list, *args, **kwargs):
        min_path_length, min_path_list = self.get_shortest(localtion_list, *args, **kwargs)
        gmp = gmplot.GoogleMapPlotter(23.973837, 120.97969, 8, apikey=self.google_api_key, title=None)
        latitude_list, longitude_list = zip(*min_path_list)

        gmp.scatter(latitude_list, longitude_list, '#FF0000',
                    size=300, marker=True)

        gmp.plot(latitude_list, longitude_list,
                'cornflowerblue', edge_width=2.5)

        return min_path_length, min_path_list, gmp.get()

    