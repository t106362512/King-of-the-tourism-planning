from backend.resource.datatable_server_side.serverside_table import ServerSideTable
from backend.models.model import ScenicSpotInfo
from flask_restful import Resource, reqparse
from flask import request
import json

class ScenicSpot(Resource):


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
        result = ScenicSpotInfo.get(args)

        SERVERSIDE_TABLE_COLUMNS = [
            {
                "data_name": "Name",
                "column_name": "Name",
                "default": "",
                "order": 1,
                "searchable": True
            },
            {
                "data_name": "Toldescribe",
                "column_name": "Toldescribe",
                "default": "",
                "order": 2,
                "searchable": True
            },
            {
                "data_name": "Add",
                "column_name": "Add",
                "default": 0,
                "order": 3,
                "searchable": True
            },
            {
                "data_name": "Tel",
                "column_name": "Tel",
                "default": 0,
                "order": 4,
                "searchable": False
            }
        ]

        a = ServerSideTable(request, data=result, column_list=SERVERSIDE_TABLE_COLUMNS).output_result()
        return a
        # return {'data': result}

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