# from iteration_utilities import unique_everseen
from pymongo.errors import BulkWriteError
from mongoengine import signals  # from blinker import signal
import marshmallow_mongoengine as ma
import mongoengine as me
import logging
import requests
import json
import uuid

# from . import db as me
# from ca_backend import db

class ScenicSpotInfo(me.Document):
    # pylint: disable=no-member
    # Id = me.StringField(primary_key=True)
    # 因考量到資料數不多，故不自行建立 uuid 當 primary_key。不指定 primary_key 時，mongoedb 會自動建立 binary uuid 當 primary_key
    # _id = me.UUIDField(binary=False, default=lambda: str(uuid.uuid4()), required=True, primary_key=True)
    Id = me.StringField() # The source Id
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
        'auto_create_index': True,
        'collection': 'scenic_spot_info',
        'indexes': [{'fields': ['Id'], 'unique': True}]
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
        bulk = cls._get_collection().initialize_ordered_bulk_op()

        for info in infos:
            scenic_model = cls(**info)
            scenic_model.Location = (info['Px'], info['Py'])
            scenic_model.Keywords = info['Keyword'].split(',') if isinstance(info['Keyword'], str) else None
            bulk.find({ "Id": scenic_model['Id'] }).upsert().replace_one(scenic_model.to_mongo())
        try:
            bulk.execute()
        except BulkWriteError as bwe:
            logging.error(bwe.details)
            #you can also take this component and do more analysis
            #werrors = bwe.details['writeErrors']
            raise
        # cls.objects.insert(bulk)
        return json.loads(cls.objects.all().to_json())

    @classmethod
    def delete(cls):
        return cls.objects.delete()

class CILocation(me.Document):
    # pylint: disable=no-member
    name = me.StringField()
    description = me.StringField()
    encodingType = me.StringField()
    location = me.GeoJsonBaseField()
    station = me.StringField()
    _iot_id = me.IntField()
    _iot_selfLink = me.StringField()
    HistoricalLocations_iot_navigationLink = me.StringField()
    Things_iot_navigationLink = me.StringField()

    meta = {
        # 'indexes': [],
        'auto_create_index': True,
        'collection': 'ci_location',
        'indexes': [
            {'fields': ['_iot_selfLink'], 'unique': True}, 
            [("location", "2dsphere")] 
        ]
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
    def insert_all(cls, station='STA_Rain', **kwargs):

        url = kwargs.get('url', f'https://sta.ci.taiwan.gov.tw/{station}/v1.0/Locations')
        data_content = json.loads(requests.get(url).text)
        infos = data_content['value']
        bulk = cls._get_collection().initialize_ordered_bulk_op()
        # o_bulk = [cls(**cls._change_key_name(info)) for info in infos]

        for info in infos:
            ci_location_model = cls(**cls._change_key_name(info))
            ci_location_model.station = station
            bulk.find({ "_iot_selfLink": ci_location_model['_iot_selfLink'] }).upsert().replace_one(ci_location_model.to_mongo())
        try:
            bulk.execute()
        except BulkWriteError as bwe:
            logging.error(bwe.details)
            raise

        if '@iot.nextLink' in data_content:
            cls.insert_all(url=data_content['@iot.nextLink'])
        return json.loads(cls.objects.all().to_json())

    @classmethod
    def delete_all(cls):
        return cls.objects.delete()

class Observation(me.EmbeddedDocument):
    # pylint: disable=no-member
    phenomenonTime = me.DateTimeField()
    resultTime = me.DateTimeField()
    result = me.IntField()
    _iot_id = me.IntField()
    _iot_selfLink = me.StringField()

    def __init__(self, data, *args, **kwargs):
        {str(key).replace('.', '_').replace('@', '_'): value for key, value in data.items()}

class Datastream(me.Document):
    # pylint: disable=no-member
    name = me.StringField()
    description = me.StringField()
    station = me.StringField()
    observationType = me.StringField()
    unitOfMeasurement = me.DynamicField()
    phenomenonTime = me.StringField()
    resultTime = me.StringField()
    Sensor_iot_navigationLink = me.StringField()
    ObservedProperty_iot_navigationLink = me.StringField()
    Things_iot_navigationLink = me.StringField()
    Observations_iot_navigationLink = me.StringField()
    # Observations
    Observations_iot_nextLink = me.StringField()
    _iot_id = me.IntField()
    _iot_selfLink = me.StringField()

    meta = {
        # 'indexes': [],
        'auto_create_index': True,
        'collection': 'ci_datastream',
        'indexes': [
            {'fields': ['_iot_selfLink'], 'unique': True}
        ]
    }

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        logging.debug("Pre Save: %s" % document.name)


    @classmethod
    def _change_key_name(cls, data, **kwargs):
        if isinstance(data, dict):
            lambda x: x
            return {str(key).replace('.', '_').replace('@', '_'): value for key, value in data.items()}