from models.model import FullDatastream#, Datastreams, Observations
from models.database import Database
from pprint import pprint
import requests
import unittest
import json
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
            "$top": 3
        }
        r = requests.get(url=ep, params=pa).text
        result = FullDatastream().loads(r)['value']
        status = Database.save_to_db(result)
        pprint(result)

        assert status is not None

    def test_4_spot(self):
        ep = 'https://gis.taiwan.net.tw/XMLReleaseALL_public/scenic_spot_C_f.json'
        r = requests.get(url=ep).text
        raw = json.loads(r)
        Database.save_to_db(raw['XML_Head'])
        print(raw)
        # infos = json.loads(r)
        # result = Observations().loads(r).data
        # pprint(result)

        # assert result is not None
