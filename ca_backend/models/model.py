from marshmallow import Schema, fields, pre_dump, pre_load, post_dump, post_load, INCLUDE, RAISE, EXCLUDE
from json import JSONEncoder
import marshmallow_mongoengine as ma
import mongoengine as me
import requests
import json
# from . import db as me
# from ca_backend import db


class Base(Schema):

    Locations_iot_navigationLink = fields.URL()
    HistoricalLocations_iot_navigationLink = fields.URL()
    Datastreams_iot_navigationLink = fields.URL()
    MultiDatastreams_iot_navigationLink = fields.URL()
    _iot_id = fields.Int()
    _iot_selfLink = fields.URL()
    _iot_nextLink = fields.URL()
    _iot_count = fields.Int()

    @pre_load
    def change_key_name(self, data, **kwargs):
        if isinstance(data, dict):
            return {str(key).replace('.', '_').replace('@', '_'): value for key, value in data.items()}


class LocationM(Base):
    class Meta:
        unknown = True
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    encodingType = fields.Str(required=True)
    location = fields.Raw(required=True)


class Observation(Base):
    class Meta:
        unknown = True
    phenomenonTime = fields.DateTime()
    resultTime = fields.Str(allow_none=True)
    result = fields.Raw()
    properties = fields.Raw()


class Thing(Base):
    class Meta:
        unknown = True
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    properties = fields.Raw()


class Datastream(Base):
    class Meta:
        unknown = True
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    observationType = fields.URL()
    unitOfMeasurement = fields.Raw()
    phenomenonTime = fields.Str()
    phenomenon_time_start = fields.DateTime()
    phenomenon_time_end = fields.DateTime()

    @pre_load
    def spilt_phenomenonTime(self, data, **kwargs):
        if 'phenomenonTime' in data:
            (data['phenomenon_time_start'], data['phenomenon_time_end']) = str(
                data['phenomenonTime']).split('/')
            return data

class LocationsInThing(Thing):
    Locations = fields.List(fields.Nested(LocationM))


class ThingAndLocationInDatastream(Datastream):
    Observations = fields.List(fields.Nested(
        Observation), data_key='Observations')
    Thing = fields.Nested(LocationsInThing, data_key='Thing')


class FullDatastream(Schema):
    # class Meta:
    #     fields = ('value')
    _iot_count = fields.Int(data_key='@iot.count')
    _iot_nextLink = fields.URL(data_key='@iot.nextLink')
    value = fields.List(fields.Nested(ThingAndLocationInDatastream))


class ScenicSpotInfo(me.Document):
    # pylint: disable=no-member
    Id = me.StringField(primary_key=True)
    Name = me.StringField()
    Zone = me.StringField()
    Toldescribe = me.StringField()
    Description = me.StringField()
    Tel = me.StringField()
    Add = me.StringField()
    Zipcode = me.StringField()
    Region = me.StringField()
    Town = me.StringField()
    Travellinginfo = me.StringField()
    Opentime = me.StringField()
    Picture1 = me.StringField()
    Picdescribe1 = me.StringField()
    Picture2 = me.StringField()
    Picdescribe2 = me.StringField()
    Picture3 = me.StringField()
    Picdescribe3 = me.StringField()
    Map = me.StringField()
    Gov = me.StringField()
    Px = me.FloatField()
    Py = me.FloatField()
    Orgclass = me.StringField()
    Class1 = me.StringField()
    Class2 = me.StringField()
    Class3 = me.StringField()
    Level = me.StringField()
    Website = me.StringField()
    Parkinginfo = me.StringField()
    Parkinginfo_Px = me.FloatField()
    Parkinginfo_Py = me.FloatField()
    Ticketinfo = me.StringField()
    Remarks = me.StringField()
    Keyword = me.StringField()
    Changetime = me.DateTimeField()
    Location = me.GeoPointField()
    Keywords = me.ListField()

    meta = {
        # 'indexes': [
        # {
        #     'fields': ['$Name', "$Toldescribe"],
        #     'default_language': 'english',
        #     'weights': {'Name': 5, 'Toldescribe': 10}
        #  }
        # ],
        'auto_create_index': True
    }

    def __repr__(self):
        return '<ScenicSpotInfo(name={self.name!r})>'.format(self=self)

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def get(args:dict):
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
        return json.loads(q_set_json)
    
    @staticmethod
    def update():
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
        return json.loads(ScenicSpotInfo.objects.all().to_json())

    @staticmethod
    def delete():
        return ScenicSpotInfo.objects.delete()
