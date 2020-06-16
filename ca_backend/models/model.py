from json import JSONEncoder
# from iteration_utilities import unique_everseen
from mongoengine import signals
import marshmallow_mongoengine as ma
import mongoengine as me
import requests
import json

# from . import db as me
# from ca_backend import db

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

    @classmethod
    def get(cls, args:dict):
        raw_query = {
            'Name': args['Name'],
            'Toldescribe__icontains': args['Keyword'],
            'Ticketinfo__icontains': args['Ticketinfo'],
            'Travellinginfo__icontains': args['Travellinginfo'],
            'Add__icontains': args['Add'],
            # 'Location__geo_within_center': [args['Location'].split(','), args['Distance']] if args['Location'] and args['Distance'] else None,
            # 'Location__geo_within_sphere': [args['Location'].split(','), args['Distance']] if args['Location'] and args['Distance'] else None
            'Location__near': list(map(float, args['Location'].split(','))) if args['Location'] else None,
            'Location__max_distance': float(args['Distance']) if args['Distance'] and args['Location'] else None
        }
        query = dict(filter(lambda item: item[1] is not None or False, raw_query.items()))
        q_set_json = cls.objects(**query).to_json()
        return json.loads(q_set_json)
    
    @classmethod
    def insert_all(cls):
        url = 'https://gis.taiwan.net.tw/XMLReleaseALL_public/scenic_spot_C_f.json'
        content = requests.get(url).text
        infos = json.loads(content)['XML_Head']['Infos']['Info']
        bulk = []
        # mongo_data = cls.objects.only('Id').as_pymongo()#.to_json()
        # all = [user._id for user in mongo_data._iter_results()]
        # print(all)

        for info in infos:
            s = cls(**info)
            s.Location = (info['Px'], info['Py'])
            s.Keywords = info['Keyword'].split(',') if isinstance(info['Keyword'], str) else None
            bulk.append(s)
            
        cls.objects.insert(bulk)
        return json.loads(cls.objects.all().to_json())
        # return cls.objects.all().to_mongo().to_dict()

    @classmethod
    def delete(cls):
        return cls.objects.delete()

class CILocation(me.Document):
    # pylint: disable=no-member
    name = me.StringField()
    description = me.StringField()
    encodingType = me.StringField()
    location = me.GeoJsonBaseField()
    _iot_id = me.IntField()
    _iot_selfLink = me.StringField(primary_key=True)
    HistoricalLocations_iot_navigationLink = me.StringField()
    Things_iot_navigationLink = me.StringField()

    meta = {
        'indexes': [[("location", "2dsphere")]],
        'auto_create_index': True
    }

    @classmethod
    def _change_key_name(cls, data, **kwargs):
        if isinstance(data, dict):
            return {str(key).replace('.', '_').replace('@', '_'): value for key, value in data.items()}

    @classmethod
    def get(cls, args:dict):
        raw_query = {
            'location__geo_within_center': [list(map(float, args['Location'].split(','))), float(args['Distance'])] if args['Location'] and args['Distance'] else None,
            # 'location__geo_within_sphere': [list(map(float, args['Location'].split(','))), float(args['Distance'])] if args['Location'] and args['Distance'] else None
        }
        query = dict(filter(lambda item: item[1] is not None or False, raw_query.items()))
        q_set_json = cls.objects(**query).to_json()
        return json.loads(q_set_json)

    @classmethod
    def get_info(cls):
        pass

    @classmethod
    def insert_all(cls, station='STA_Rain', **kwargs):
        url = kwargs.get('url', f'https://sta.ci.taiwan.gov.tw/{station}/v1.0/Locations')
        data_content = json.loads(requests.get(url).text)
        infos = data_content['value']
        bulk = [cls(**cls._change_key_name(info)) for info in infos]
        cls.objects.insert(bulk)
        if '@iot.nextLink' in data_content:
            cls.insert_all(url=data_content['@iot.nextLink'])
        return json.loads(cls.objects.all().to_json())

    @classmethod
    def delete_all(cls):
        return cls.objects.delete()