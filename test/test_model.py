from ca_backend.models.model import FullDatastream, Datastreams, Observations
from ca_backend.models.database import Database
from pprint import pprint
import requests
import unittest
import os



class TestModel(unittest.TestCase):
    
    def setUp(self):
        mcs = os.getenv('MONGODB_CONNECTIONSTRING')
        Database.initialize(mcs)

    def test_1_FullDatastream(self):
        ep = 'https://sta.ci.taiwan.gov.tw/STA_AirQuality_v2/v1.0/Datastreams'
        pa = {
            "$expand": "Thing,Thing/Locations,Observations",
            "$filter": "st_equals(Thing/Locations/location,geography'POINT(121.7601 25.1292)')",
            "$count": "true",
            "$top": 3
        }
        r = requests.get(url=ep, params=pa).text
        result = FullDatastream().loads(r).data
        pprint(result)
        status = Database.save_to_db(result)
        pprint(status)

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
        result = Datastreams().loads(r).data
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
        result = Observations().loads(r).data
        pprint(result)

        assert result is not None
