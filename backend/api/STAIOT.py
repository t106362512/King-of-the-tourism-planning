from flask_restful import Resource, reqparse
from backend.models.model import CILocation, Datastream

class STALoc(Resource):
    
    def get(self):
        # 根據旅遊位置及該旅遊位置的半徑距離，以找出附近的氣象站位置。
        # 1. 先將“Location: 旅遊地點經緯度”與”Distance: 旅遊地點半徑範圍“傳送給以下端點
        # http://127.0.0.1:5000/api/location?Location=121.55292, 25.27472&Distance=0.05
        # 2. 隨後會收到以下結果, 需記下 coordinates 資訊, 以post到下一端點
        # [
        #     {
        #         "_id": {
        #             "$oid": "5eef0890db9b76aa90e69ad7"
        #         },
        #         "name": "雨量站-01A350-新北市石門區富貴角",
        #         "description": "雨量站-01A350-新北市石門區富貴角",
        #         "encodingType": "application/vnd.geo+json",
        #         "location": {
        #             "type": "Point",
        #             "coordinates": [
        #                 121.5359,
        #                 25.2903
        #             ]
        #         },
        #         "station": "STA_Rain",
        #         "_iot_id": 74,
        #         "_iot_selfLink": "https://sta.ci.taiwan.gov.tw/STA_Rain/v1.0/Locations(74)",
        #         "HistoricalLocations_iot_navigationLink": "https://sta.ci.taiwan.gov.tw/STA_Rain/v1.0/Locations(74)/HistoricalLocations",
        #         "Things_iot_navigationLink": "https://sta.ci.taiwan.gov.tw/STA_Rain/v1.0/Locations(74)/Things"
        #     }
        # ]

        parser = reqparse.RequestParser()
        parser.add_argument('Station', type=str, default="STA_Rain")
        parser.add_argument('Location', type=str, default=None, help='plz type like the 121.297187,24.943325')
        parser.add_argument('Distance', type=str, default=None)
        args = parser.parse_args()
        result = CILocation.get(args)
        return result

    def post(self):
        # pylint: disable=no-member
        # 1. 根據 get 得到的 coordinates (121.5359,25.2903) 後,再將該資訊打進以下網址的 Location
        # 2. 可得到相關資訊
        # http://127.0.0.1:5000/api/location?Location=121.5359,25.2903
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str, default=None)
        parser.add_argument('Station', type=str, default='STA_Rain')
        parser.add_argument('Location', type=str, default=None, required=True, help='plz type like the 121.4946,24.7783')
        args = parser.parse_args()
        station = args['Station']
        location = args['Location']
        # return Datastream.insert_all(station, location)
        if(CILocation.objects(station__in=station).count() < 0):
            CILocation.insert_all(station)
        return Datastream.get_station_info(station, location)

        # try:
        #     return Datastream.get_station_info(station, location)
        # except pymongo.errors.InvalidOperation as e:
        #     if(CILocation.objects(station__in=station).count() < 0):
        #         CILocation.insert_all(station)
        #         return Datastream.get_station_info(station, location)
        #     else:
        #         return {'data': 'error'}

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str, default=None)
        parser.add_argument('station', type=str, default='STA_Rain')
        args = parser.parse_args()
        station = args['Station']
        return CILocation.insert_all(station)

    def delete(self):
        result = CILocation.delete_all()
        return {'collection': result, 'status': "successed"}

