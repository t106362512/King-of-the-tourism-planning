# from ..models.RoutePlaningModel import RoutePlaning
from ..resource.RoutePlanning import RoutePlanning as RP
from ..models.model import ScenicSpotInfo, CILocation, Datastream
from flask_restful import Resource, reqparse
import requests
import json
import re
import threading
import time
from queue import Queue

class RoutePlanning(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('LocationList', type=str, default=None, action='append', help='plz type like the [121.297187,24.943325]')
        args = parser.parse_args()
        Location_list = args['LocationList']
        min_path_length, min_path_list = RP().get_shortest(Location_list)
        result = {'MinPathLen': min_path_length, 'MinPathList': min_path_length}
        return result

    def post(self):
        # pylint: disable=no-member
        import pdb; pdb.set_trace()
        parser = reqparse.RequestParser()
        parser.add_argument('Location', type=str, default=None, action='append', help='plz type like the "121.297187,24.943325"')
        parser.add_argument('Id', type=str, default=None, action='append', help='plz type like the "C1_313020000G_000026"')
        raw_args = parser.parse_args()
        print(raw_args)
        Inside = 'Location' if raw_args['Location'] else 'Id'
        result_list = []
        while raw_args[Inside]:
            args = {Inside: raw_args[Inside].pop()}
            info_dict = {}
            info_dict['ScenicSpotInfo'] = (ScenicSpotInfo.get(args))
            for sta in ['STA_AirQuality_v2', 'STA_Rain']:
                # check if not have any station location, then insert all.
                if(CILocation.objects(station=sta).count() == 0):
                    CILocation.insert_all(sta)
                loc_array = CILocation.get({**args, 'Station': sta, 'Distance': 0.05})[0]['location']['coordinates']
                sta_info = Datastream.get_station_info(sta, ','.join(map(str, loc_array)))
                info_dict[sta] = sta_info
            result_list.append(info_dict)
        return result_list

    def post_single(self):
        # pylint: disable=no-member
        parser = reqparse.RequestParser()
        parser.add_argument('Location', type=str, default=None, help='plz type like the "121.297187,24.943325"')
        parser.add_argument('Id', type=str, default=None, help='plz type like the "C1_313020000G_000026"')
        args = parser.parse_args()
        result_dict = {}
        result_dict['ScenicSpotInfo'] = (ScenicSpotInfo.get(args))
        for sta in ['STA_AirQuality_v2', 'STA_Rain']:
            # check if not have any station location, then insert all.
            if(CILocation.objects(station=sta).count() == 0):
                CILocation.insert_all(sta)
            loc_array = CILocation.get({**args, 'Station': sta, 'Distance': 0.05})[0]['location']['coordinates']
            sta_info = Datastream.get_station_info(sta, ','.join(map(str, loc_array)))
            result_dict[sta] = sta_info
        return result_dict


    def put(self):
        pass

    def delete(self):
        pass
