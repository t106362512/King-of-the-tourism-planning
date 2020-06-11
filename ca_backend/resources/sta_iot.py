from flask_restful import Resource, reqparse
from ..models.database import Database
from ..models.model import FullDatastream
import requests

class STA(Resource):
    
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str, default=None)
        args = parser.parse_args()
        pa = {
            "$expand": "Thing,Thing/Locations,Observations",
            "$filter": "st_equals(Thing/Locations/location,geography'POINT(121.7601 25.1292)')",
            "$top": 3
        }
        content = requests.get(args['url'], params=pa).text
        result = FullDatastream().loads(content).data
        Database.save_to_db(result)
        return result

    def delete(self):
        pass