from flask_restful import Resource, reqparse
from ..models.model import CILocation
from ..models.database import Database
# from ..models.pre import FullDatastream
import requests

class STALoc(Resource):
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Location', type=str, default=None, help='plz type like the 121.297187,24.943325')
        parser.add_argument('Distance', type=float, default=None, help='plz type the number')
        args = parser.parse_args()
        result = CILocation.get(args)
        return result

    def post(self):
        pass

    def put(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument('url', type=str, default=None)
        # args = parser.parse_args()
        # pa = {
        #     "$expand": "Thing,Thing/Locations,Observations",
        #     "$filter": "st_equals(Thing/Locations/location,geography'POINT(121.7601 25.1292)')",
        #     "$top": 3
        # }
        # content = requests.get(args['url'], params=pa).text
        # result = FullDatastream().loads(content).data
        # Database.save_to_db(result)
        # return result
        return CILocation.insert_all()

    def delete(self):
        result = CILocation.delete_all()
        return {'collection': result, 'status': "successed"}

