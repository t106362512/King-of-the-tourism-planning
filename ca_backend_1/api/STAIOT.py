from flask_restful import Resource, reqparse
from ..models.model import CILocation, Datastream
from ..models.database import Database
import requests
import json

class STALoc(Resource):
    
    def get(self):
        # 根據旅遊位置及該旅遊位置的半徑距離，以找出附近的氣象站位置。
        parser = reqparse.RequestParser()
        parser.add_argument('station', type=str, default="STA_Rain")
        parser.add_argument('Location', type=str, default=None, help='plz type like the 121.297187,24.943325')
        parser.add_argument('Distance', type=str, default=None)
        args = parser.parse_args()
        result = CILocation.get(args)
        return result

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str, default=None)
        parser.add_argument('station', type=str, default="STA_Rain", required=True)
        parser.add_argument('Location', type=str, default=None, required=True, help='plz type like the 121.4946,24.7783')
        args = parser.parse_args()
        station = args['station']
        location = args['Location']
        # return Datastream.insert_all(station, location)
        return Datastream.insert_all(station, location)



    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str, default=None)
        parser.add_argument('station', type=str, default='STA_Rain')
        args = parser.parse_args()
        station = args['station']
        # pa = {
        #     "$expand": "Thing,Thing/Locations,Observations",
        #     "$filter": "st_equals(Thing/Locations/location,geography'POINT(121.7601 25.1292)')",
        #     "$top": 3
        # }
        # content = requests.get(args['url'], params=pa).text
        # result = FullDatastream().loads(content).data
        # Database.save_to_db(result)
        # return result
        return CILocation.insert_all(station)
        # return CILocation.insert_all(station)

    def delete(self):
        result = CILocation.delete_all()
        return {'collection': result, 'status': "successed"}

