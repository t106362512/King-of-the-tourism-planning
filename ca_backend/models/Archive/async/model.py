# from iteration_utilities import unique_everseen
from pymongo.errors import BulkWriteError
from mongoengine import signals  # from blinker import signal
import marshmallow_mongoengine as ma
import multiprocessing
import mongoengine as me
import asyncio
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

        # @background
        def task(info:dict, bulk):
            scenic_model = cls(**info)
            scenic_model.Location = (info['Px'], info['Py'])
            scenic_model.Keywords = info['Keyword'].split(',') if isinstance(info['Keyword'], str) else None
            bulk.find({ "Id": scenic_model['Id'] }).upsert().replace_one(scenic_model.to_mongo())

        for info in infos:
            asyncio.set_event_loop(asyncio.new_event_loop())
            task(info, bulk)

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
    datastreamList = me.ListField()
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

    def __init__(self, *args, **kwargs):
        # blinker signals 無法應用在 bulk.find().upsert().replace_one(), 故直接改 init
        kwargs = {str(key).replace('.', '_').replace('@', '_'): value for key, value in kwargs.items()}
        super(CILocation, self).__init__(*args, **kwargs)

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
    def background(cls,f):
        def wrapped(*args, **kwargs):
            return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)
        return wrapped


    @classmethod
    def insert_all(cls, station, **kwargs):

        url = kwargs.get('url', f'https://sta.ci.taiwan.gov.tw/{station}/v1.0/Locations')
        data_content = json.loads(requests.get(url).text)
        infos = data_content['value']
        bulk = cls._get_collection().initialize_ordered_bulk_op()

        @cls.background
        def task(info:dict, bulk):
            th_url = info['Things@iot.navigationLink']
            ds_url = json.loads(requests.get(th_url).text)['value'][0]['Datastreams@iot.navigationLink']
            ds_list = [ds['@iot.selfLink'] for ds in json.loads(requests.get(ds_url).text)['value']]
            # print(ds_list)
            ci_location_model = cls(**info)
            ci_location_model.station = station
            ci_location_model.datastreamList = ds_list
            bulk.find({ "_iot_selfLink": ci_location_model['_iot_selfLink'] }).upsert().replace_one(ci_location_model.to_mongo())
            return ci_location_model

        # async def __async__get_ticks():
        #     async with wws as echo:
        #         await echo.send(json.dumps({'ticks_history': 'R_50', 'end': 'latest', 'count': 1}))
        #         return await echo.receive()

        for idx, info in enumerate(infos):
            asyncio.set_event_loop(asyncio.new_event_loop())
            task(info, bulk)
            asyncio.get_event_loop().run_until_complete(len(bulk.__bulk.ops)==idx)
            
        try:
            bulk.execute()
        except BulkWriteError as bwe:
            logging.error(bwe.details)
            raise
        if '@iot.nextLink' in data_content:
            cls.insert_all(station, url=data_content['@iot.nextLink'])
        
        asyncio.get_event_loop().close()
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

    meta = {
        'auto_create_index': True,
        'collection': 'ci_observation',
        'indexes': [
            {'fields': ['_iot_selfLink'], 'unique': True}
        ]
    }

    def __init__(self, data, *args, **kwargs):
        kwargs = {str(key).replace('.', '_').replace('@', '_'): value for key, value in data.items()}
        super(Observation, self).__init__(*args, **kwargs)

    
    # @classmethod
    # def pre_init(cls, sender, document, **kwargs):
    #     # logging.info("Pre Save: %s" % document.name)
    #     print("Pre %s" % document)
    #     print("Pre Save: %s" % document)


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
    Observations = me.EmbeddedDocumentListField(Observation)
    Observations_iot_nextLink = me.StringField()
    _iot_id = me.IntField()
    _iot_selfLink = me.StringField()

    meta = {
        'auto_create_index': True,
        'collection': 'ci_datastream',
        'indexes': [
            {'fields': ['_iot_selfLink'], 'unique': True}
        ]
    }

    def __init__(self, *args, **kwargs):
        kwargs = {str(key).replace('.', '_').replace('@', '_'): value for key, value in kwargs.items()}
        super(Datastream, self).__init__(*args, **kwargs)
    

# signals.pre_init.connect(Observation.pre_init, sender=Observation)