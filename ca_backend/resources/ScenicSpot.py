from models.model import ScenicSpotInfo
from models.database import Database
from flask_restful import Resource, reqparse
import requests
import json
import re

class ScenicSpot_resource(Resource):


    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Name', type=str, default=None)
        parser.add_argument('Keyword', type=str, default=None)
        parser.add_argument('Ticketinfo', type=str, default=None)
        parser.add_argument('Travellinginfo', type=str, default=None)
        parser.add_argument('Add', type=str, default=None)
        parser.add_argument('Location', type=str, default=None, help='plz type like the 121.297187,24.943325')
        parser.add_argument('Distance', type=float, default=None, help='plz type the number')
        args = parser.parse_args()
        raw_query = {
            'Name': args['Name'],
            'Toldescribe__icontains': args['Keyword'],
            'Ticketinfo__icontains': args['Ticketinfo'],
            'Travellinginfo__icontains': args['Travellinginfo'],
            'Add__icontains': args['Add'],
            # 'Location__geo_within_center': [args['Location'].split(','), args['Distance']] if args['Location'] and args['Distance'] else None,
            # 'Location__geo_within_sphere': [args['Location'].split(','), args['Distance']] if args['Location'] and args['Distance'] else None
            'Location__near': list(map(float, args['Location'].split(','))),
            'Location__max_distance': float(args['Distance'])
        }
        query = dict(filter(lambda item: item[1] is not None or False, raw_query.items()))
        q_set_json = ScenicSpotInfo.objects(**query).to_json()
        result = json.loads(q_set_json)
        return result

    def post(self):
        pass

    def put(self):
        url = 'https://gis.taiwan.net.tw/XMLReleaseALL_public/scenic_spot_C_f.json'
        content = requests.get(url).text
        result = json.loads(content)['XML_Head']['Infos']['Info']
        bulk = []
        for info in result:
            s = ScenicSpotInfo(**info)
            s.Location = (info['Px'], info['Py'])
            s.Keywords = info['Keyword'].split(',') if isinstance(info['Keyword'], str) else None
            bulk.append(s)
        ScenicSpotInfo.objects.insert(bulk)
        return result

    def delete(self):
        result = ScenicSpotInfo.objects.delete()
        return {'collection': result, 'status': "successed"}
