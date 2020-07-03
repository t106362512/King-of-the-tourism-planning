from backend.models.model import ScenicSpotInfo
from flask_restful import Resource, reqparse
from flask import request
from backend import cache
import urllib
import json

def cache_key():
    args = request.args
    key = request.path + '?' + urllib.parse.urlencode([(k, v) for k in sorted(args) if k != '_' for v in sorted(args.getlist(k))])
    print(key)
    return key

class ScenicSpot(Resource):

    @cache.cached(timeout=604800,  key_prefix=cache_key)
    # @cache.cached(timeout=604800)
    def get(self, **kwargs):
        parser = reqparse.RequestParser()
        parser.add_argument('Name', type=str, default=None)
        parser.add_argument('Keyword', type=str, default=None)
        parser.add_argument('Ticketinfo', type=str, default=None)
        parser.add_argument('Travellinginfo', type=str, default=None)
        parser.add_argument('Add', type=str, default=None)
        parser.add_argument('Location', type=str, default=None, help='plz type like the 121.297187,24.943325')
        parser.add_argument('Distance', type=float, default=None, help='plz type the number')
        args = parser.parse_args()
        result = ScenicSpotInfo.get(args)
        return {'data': result}

    def post(self, **kwargs):
        # pylint: disable=no-member
        """
        Input list in json body.
        {
            "IdList":["C1_382000000A_402683", "C1_376430000A_000136"]
        }
        """
        RETURN_FIELDS = ["Location", "Name", "Id"]
        parser = reqparse.RequestParser()
        parser.add_argument('IdList', type=str, default=None, action='append')
        args = kwargs.get('args_dict', parser.parse_args()) 
        result_dict = json.loads(ScenicSpotInfo.objects(Id__in=args['IdList']).only(*RETURN_FIELDS).to_json())
        result = result_dict
        return {'data': result}

    def put(self):
        cache.clear() 
        result = ScenicSpotInfo.insert_all()
        return {'data': result}

    def delete(self):
        cache.clear()
        result = {'collection': ScenicSpotInfo.delete(), 'status': "successed"}
        return {'data': result}
