# from iteration_utilities import unique_everseen
from collections import defaultdict
from pymongo.errors import BulkWriteError
from mongoengine import signals  # from blinker import signal
from backend import me
from queue import Queue
# import mongoengine as me
import asyncio
import logging
import requests
import json
import re


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
        'indexes': [
                {'fields': ['Id', 'Name'], 'unique': True},
                {'fields': ['Toldescribe', 'Ticketinfo', 'Travellinginfo', 'Add', 'Region'], 'unique': False},
                [("Location", "2d")] 
            ]
    }

    def __repr__(self):
        return '<ScenicSpotInfo(name={self.name!r})>'.format(self=self)

    def to_dict(self):
        return self.__dict__

    @classmethod
    def get(cls, args:dict):
        args = defaultdict(lambda: None, args)
        # only_fields = ['Id', 'Name', 'Toldescribe', 'Description', 'Tel', 'Add', 'Region', 'Town', 'Travellinginfo', 'Opentime', 'Picture1', 'Picdescribe1', 'Ticketinfo', 'Keyword', 'Location']
        only_fields = ['Id','Name', 'Toldescribe', 'Add', 'Tel', 'Location']
        raw_query = {
            'Name': args['Name'],
            'Id': args['Id'],
            'Toldescribe__icontains': args['Keyword'],
            'Ticketinfo__icontains': args['Ticketinfo'],
            'Travellinginfo__icontains': args['Travellinginfo'],
            'Add__icontains': args['Add'],
            'Add__not': re.compile('.*(金門縣|澎湖|綠島|小琉球|馬祖|蘭嶼|連江).*'),
            'Region__not': re.compile('.*(金門縣|連江縣|澎湖縣).*'),
            # 'Location__geo_within_center': [args['Location'].split(','), args['Distance']] if args['Location'] and args['Distance'] else None,
            # 'Location__geo_within_sphere': [args['Location'].split(','), args['Distance']] if args['Location'] and args['Distance'] else None
            'Location__near': list(map(float, args['Location'].split(','))) if isinstance(args['Location'], str) else None,
            'Location__max_distance': float(args['Distance']) if isinstance(args['Distance'], (str,float)) and isinstance(args['Location'], str) else 0 if isinstance(args['Location'], str) else None 
            # 'Location__max_distance': float(args['Distance']) if isinstance(args['Distance'], str) and isinstance(args['Location'], str) else None
        }
        query = dict(filter(lambda item: item[1] is not None or False, raw_query.items()))
        if(cls.objects.count() == 0):
            cls.insert_all()
        q_set_json = cls.objects(**query).only(*only_fields).exclude('id').to_json()
        return json.loads(q_set_json)
    
    @classmethod
    def insert_all(cls):

        url = 'https://gis.taiwan.net.tw/XMLReleaseALL_public/scenic_spot_C_f.json'
        content = requests.get(url).text
        infos = json.loads(content)['XML_Head']['Infos']['Info']
        bulk = cls._get_collection().initialize_ordered_bulk_op()

        for info in infos:
            kws = info['Keyword'].split(',') if isinstance(info['Keyword'], str) else None
            scenic_model = cls(Keywords=kws, Location=(info['Px'], info['Py']), **info)
            bulk.find({ "Id": scenic_model['Id'] }).upsert().replace_one(scenic_model.to_mongo())
        try:
            bulk.execute()
        except BulkWriteError as bwe:
            logging.error(bwe.details)
            raise
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
        'auto_create_index': True,
        'collection': 'ci_location',
        'indexes': [
            {'fields': ['_iot_selfLink'], 'unique': True}, 
            {'fields': ['station'], 'unique': False}, 
            [("location", "2dsphere")] 
        ]
    }

    def __init__(self, *args, **kwargs):
        # blinker signals 無法應用在 bulk.find().upsert().replace_one(), 故直接改 init
        kwargs = {str(key).replace('.', '_').replace('@', '_'): value for key, value in kwargs.items()}
        super(CILocation, self).__init__(*args, **kwargs)
    
    @classmethod
    def get(cls, args:dict, result_limit=1) -> dict:
        args = defaultdict(lambda: None, args)
        raw_query = {
            'station__icontains': args['Station'],
            # 'location__near': list(map(float, args['Location'].split(','))) if isinstance(args['Location'], str) else args['Location'] if isinstance(args['Location'], list) else None ,
            # 'location__max_distance': float(args['Distance']) if isinstance(args['Distance'], (str,int,float)) and isinstance(args['Location'], (str,list)) else 0 if isinstance(args['Location'], (str,list)) else None 
            'location__geo_within_center': [list(map(float, args['Location'].split(',') if isinstance(args['Location'], str) else args['Location'])), float(args['Distance'])] if isinstance(args['Distance'], (str,float,int)) and isinstance(args['Location'], (str,list)) else None,
            # 'location__geo_within_sphere': [list(map(float, args['Location'].split(','))), float(args['Distance'])] if args['Location'] and args['Distance'] else None
        }

        query = dict(filter(lambda item: item[1] is not None or False, raw_query.items()))
        q_set_json = cls.objects(**query).limit(result_limit).to_json()
        return json.loads(q_set_json)

    @classmethod
    def insert_all(cls, station, **kwargs):

        url = kwargs.get('url', f'https://sta.ci.taiwan.gov.tw/{station}/v1.0/Locations')
        data_content = json.loads(requests.get(url).text)
        infos = data_content['value']
        bulk = cls._get_collection().initialize_ordered_bulk_op()

        for info in infos:
            if info['location']['type'] == 'Point':
                ci_location_model = cls(station=station, **info)
                bulk.find({ "_iot_selfLink": ci_location_model['_iot_selfLink'] }).upsert().replace_one(ci_location_model.to_mongo())
        try:
            bulk.execute()
        except BulkWriteError as bwe:
            logging.error(bwe.details)
            raise

        if '@iot.nextLink' in data_content:
            cls.insert_all(station, url=data_content['@iot.nextLink'])
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
            {'fields': ['_iot_selfLink', 'phenomenonTime', 'resultTime'], 'unique': True}
        ]
    }

    def __init__(self, *args, **kwargs):
        kwargs = {str(key).replace('.', '_').replace('@', '_'): value for key, value in kwargs.items()}
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
    Thing_iot_navigationLink = me.StringField()
    Observations_iot_navigationLink = me.StringField()
    Observations = me.EmbeddedDocumentListField(Observation)
    Observations_iot_nextLink = me.StringField()
    _iot_id = me.IntField()
    _iot_selfLink = me.StringField()
    Location = me.GeoPointField()
    loc_refer = me.ReferenceField(CILocation, dbref=True)
    ObservatoryName = me.StringField()

    meta = {
        'auto_create_index': True,
        'collection': 'ci_datastream',
        'indexes': [
            {'fields': ['_iot_selfLink'], 'unique': True},
            {'fields': ['name'], 'unique': False},
            [("Location", "2dsphere")] 
        ]
    }

    def __init__(self, *args, **kwargs):
        kwargs = {str(key).replace('.', '_').replace('@', '_'): value for key, value in kwargs.items()}
        super(Datastream, self).__init__(*args, **kwargs)

    @classmethod
    def background(cls,f):
        def wrapped(*args, **kwargs):
            return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)
        return wrapped

    @classmethod
    def get_station_info(cls, station:str, location:str, **kwargs):

        url = kwargs.get('url', f'https://sta.ci.taiwan.gov.tw/{station}/v1.0/Datastreams')
        loc = location.replace(' ', '').replace(',',' ')
        loc_for_mongo = tuple(map(float, location.split(',')))
        payload = {
            "$expand": "Observations($orderby=phenomenonTime desc;$top=1)",
            "$filter": f"st_within(Thing/Locations/location, geography'POINT ({loc})')"
        }
        data_content = json.loads(requests.get(url, params=payload).text)
        infos = data_content['value']
        bulk = cls._get_collection().initialize_ordered_bulk_op()

        for info in infos:
            obss = [Observation(**i).to_mongo() for i in info.pop('Observations')]
            loc_refer_obj = CILocation.objects(station=station, location__near=loc_for_mongo).first()
            ci_datastream_model = cls(ObservatoryName=loc_refer_obj.name, station=station, Location=loc_for_mongo, loc_refer=loc_refer_obj, **info)
            # Tricky solution, u can update the entire document and retain and accumulate nested items.
            ci_datastream_model_mod = ci_datastream_model.to_mongo()
            ci_datastream_model_mod.pop('Observations')
            bulk.find({ "_iot_selfLink": ci_datastream_model['_iot_selfLink'] }).upsert().update_one({'$set':ci_datastream_model_mod})
            for obs in obss:
                # print(obs)
                bulk.find({"_iot_selfLink": ci_datastream_model['_iot_selfLink']}).upsert().update_one({'$addToSet':{'Observations': obs}})

        try:
            bulk.execute()
        except BulkWriteError as bwe:
            logging.error(bwe.details)
            raise

        if '@iot.nextLink' in data_content:
            cls.insert_all(station, location, url=data_content['@iot.nextLink'])

        pipeline = [
            {
                "$match": {
                    "station" : station,
                    "Location": loc_for_mongo
                } 
            },
            {
                "$project": {
                    '_id': False,
                    "name": 1,
                    "description": 1,
                    "ObservatoryName": 1,
                    "station": 1,
                    "Location": 1,
                    "unitOfMeasurement": 1,
                    "Observations": {
                        "$filter": {
                            "input": "$Observations",
                            "cond": { 
                                "$eq": [
                                    {
                                        "$max": "$Observations.phenomenonTime"
                                    },
                                    "$$this.phenomenonTime"
                                ]
                            }
                        }
                    }
                } 
            },
            {
                "$addFields": {
                    "Observations": {
                        "$map": {
                            "input": "$Observations",
                            "in": {
                                "phenomenonTime": {
                                    "$dateToString":{"date":"$$this.phenomenonTime"}
                                },
                                "result": "$$this.result",
                                "_iot_id": "$$this._iot_id",
                                "_iot_selfLink": "$$this._iot_selfLink"
                            }
                        }
                    }
                } 
            }
        ] 
        return list(cls.objects().aggregate(pipeline))

    @classmethod
    def insert_all_by_loc(cls, station:str, location:str, **kwargs):

        url = kwargs.get('url', f'https://sta.ci.taiwan.gov.tw/{station}/v1.0/Datastreams')
        loc = location.replace(' ', '').replace(',',' ')
        loc_for_mongo = tuple(map(float, location.split(',')))
        payload = {
            "$expand": "Observations($orderby=phenomenonTime desc;$top=1)",
            "$filter": f"st_within(Thing/Locations/location, geography'POINT ({loc})')"
        }
        data_content = json.loads(requests.get(url, params=payload).text)
        infos = data_content['value']
        bulk = cls._get_collection().initialize_ordered_bulk_op()

        for info in infos:
            obss = [Observation(**i).to_mongo() for i in info.pop('Observations')]
            loc_refer_obj = CILocation.objects(station=station, location__near=loc_for_mongo).first()
            ci_datastream_model = cls(station=station, Location=loc_for_mongo, loc_refer=loc_refer_obj, **info)
            # Tricky solution, u can update the entire document and retain and accumulate nested items.
            ci_datastream_model_mod = ci_datastream_model.to_mongo()
            ci_datastream_model_mod.pop('Observations')
            bulk.find({ "_iot_selfLink": ci_datastream_model['_iot_selfLink'] }).upsert().update_one({'$set':ci_datastream_model_mod})
            for obs in obss:
                bulk.find({"_iot_selfLink": ci_datastream_model['_iot_selfLink']}).upsert().update_one({'$addToSet':{'Observations': obs}})
        try:
            bulk.execute()
        except BulkWriteError as bwe:
            logging.error(bwe.details)
            raise

        if '@iot.nextLink' in data_content:
            cls.insert_all(station, location, url=data_content['@iot.nextLink'])
        return json.loads(cls.objects.all().to_json())

# signals.pre_init.connect(Observation.pre_init, sender=Observation)