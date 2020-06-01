import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.main.models import FullDatastream, Datastreams, Observations
from pprint import pprint
import requests
import unittest



class TestModel(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_1_FullDatastream(self):
        ep = 'https://sta.ci.taiwan.gov.tw/STA_AirQuality_v2/v1.0/Datastreams'
        pa = {
            "$expand": "Thing,Thing/Locations,Observations",
            "$filter": "st_equals(Thing/Locations/location,geography'POINT(121.7601 25.1292)')",
            "$count": "true",
            "$top": 3
        }
        r = requests.get(url=ep, params=pa).text
        result = FullDatastream().loads(r)
        pprint(result)

        assert result is not None

    def test_2_Datastreams(self):
        ep = 'https://sta.ci.taiwan.gov.tw/STA_AirQuality_v2/v1.0/Datastreams'
        pa = {
            # "$expand": "Thing,Thing/Locations,Observations",
            # "$filter": "st_equals(Thing/Locations/location,geography'POINT(121.7601 25.1292)')",
            "$count": "true",
            "$top": 1
        }
        r = requests.get(url=ep, params=pa).text
        result = Datastreams().loads(r)
        pprint(result)

        assert result is not None

    def test_3_Observations(self):
        ep = 'https://sta.ci.taiwan.gov.tw/STA_AirQuality_v2/v1.0/Observations'
        pa = {
            # "$expand": "Thing,Thing/Locations,Observations",
            # "$filter": "st_equals(Thing/Locations/location,geography'POINT(121.7601 25.1292)')",
            "$count": "true",
            "$top": 3
        }
        r = requests.get(url=ep, params=pa).text
        result = Observations().loads(r)
        pprint(result)

        assert result is not None
