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

        '''
        localtion_list = [[121.60546, 25.28247], [121.84354, 25.10815]]
        mode = select one from ('distance', 'duration', 'duration_in_traffic')
        mapping_list = using index mapping the mapping_list 
        '''

        now = datetime.now()
        org = list(map(lambda x: (x[1],x[0]), localtion_list))

        matrix = self.gmaps.distance_matrix(
            org,
            org,
            # mode="walking",
            mode="driving",
            language="zh-TW",
            units="metric",
            departure_time=now
        )
        min_path_length, min_path_list, min_mapping_path_list = TSP().from_gmaps_matrix(matrix, location_list=org, *args, **kwargs).normal_ans(start=0)

        return (min_path_length, min_path_list, min_mapping_path_list)

    def get_shortest_map(self, localtion_list:list, *args, **kwargs):
        '''
        localtion_list = [[121.60546, 25.28247], [121.84354, 25.10815]]
        mode = select one from ('distance', 'duration', 'duration_in_traffic')
        mapping_list = using index mapping the mapping_list 
        '''
        (min_path_length, min_path_list, min_mapping_path_list) = self.get_shortest(localtion_list, *args, **kwargs)
        gmp = gmplot.GoogleMapPlotter(23.973837, 120.97969, 8, apikey=self.google_api_key, title=None)
        latitude_list, longitude_list = zip(*min_path_list)

        gmp.scatter(latitude_list, longitude_list, '#FF0000',
                    size=300, marker=True)

        gmp.plot(latitude_list, longitude_list,
                'cornflowerblue', edge_width=2.5)

        return (min_path_length, min_path_list, min_mapping_path_list, gmp.get())

    