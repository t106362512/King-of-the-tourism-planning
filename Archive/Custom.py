from marshmallow import Schema, fields, pre_dump, pre_load, post_dump, RAISE, ValidationError
import json
import requests
import Base

class LocationsInThing(Base.Thing):
    locations = fields.List(fields.Nested(Base.Locations, only=['value']))

class ThingAndLocationInDatastream(Base.Datastream):
    observations = fields.List(fields.Nested(Base.Observations, only=['value']))
    thing = fields.Nested(LocationsInThing)

class FullDatastream(Schema):
    class Meta:
        model = ThingAndLocationInDatastream
    _iot_count = fields.Int(data_key='@iot.count')
    _iot_nextLink = fields.URL(data_key='@iot.nextLink')
    items = fields.List(fields.Nested(ThingAndLocationInDatastream), data_key='value')

# ep = 'https://sta.ci.taiwan.gov.tw/STA_AirQuality_v2/v1.0/Datastreams'
# pa = {
#     "$expand": "Thing,Thing/Locations,Observations",
#     "$filter": "st_equals(Thing/Locations/location,geography'POINT(121.7601 25.1292)')",
#     "$count": "true",
#     "$top": 3
# }
# r = requests.get(url=ep, params=pa).text
# m = FullDatastream().loads(r)
# print(m)

