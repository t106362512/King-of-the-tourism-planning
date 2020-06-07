from models.model import FullDatastream, Datastreams, Observations, ScenicSpot
from models.database import Database
from pprint import pprint
import requests
import unittest
import json
import os

if __name__ == "__main__":
    mcs = os.getenv('MONGODB_CONNECTIONSTRING')
    ep = 'https://gis.taiwan.net.tw/XMLReleaseALL_public/scenic_spot_C_f.json'
    r = requests.get(url=ep).text
    raw = json.loads(r)
    raw_s = json.dumps(raw['XML_Head']['Infos'])
    s = ScenicSpot()
    s.from_json(json_data=raw_s)
    s.save()
    # Database.save_to_db()
    print(raw)
    pass