# from iteration_utilities import unique_everseen
from pymongo.errors import BulkWriteError
from mongoengine import signals  # from blinker import signal
# import marshmallow_mongoengine as ma
import multiprocessing
import mongoengine as me
import asyncio
import logging
import requests
import json
import uuid

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

        for info in infos:
            scenic_model = cls(**info)
            scenic_model.Location = (info['Px'], info['Py'])
            scenic_model.Keywords = info['Keyword'].split(',') if isinstance(info['Keyword'], str) else None
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
    def insert_all(cls, station, **kwargs):

        url = kwargs.get('url', f'https://sta.ci.taiwan.gov.tw/{station}/v1.0/Locations')
        data_content = json.loads(requests.get(url).text)
        infos = data_content['value']
        bulk = cls._get_collection().initialize_ordered_bulk_op()

        for info in infos:
            ci_location_model = cls(**info)
            ci_location_model.station = station
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

    meta = {
        'auto_create_index': True,
        'collection': 'ci_datastream',
        'indexes': [
            {'fields': ['_iot_selfLink'], 'unique': True},
            [("Location", "2dsphere")] 
        ]
    }

    def __init__(self, *args, **kwargs):
        kwargs = {str(key).replace('.', '_').replace('@', '_'): value for key, value in kwargs.items()}
        super(Datastream, self).__init__(*args, **kwargs)


    @classmethod
    def get_station_info(cls, station:str, location:str, **kwargs):

        url = kwargs.get('url', f'https://sta.ci.taiwan.gov.tw/{station}/v1.0/Datastreams')
        loc = location.replace(',',' ')
        pa = {
            "$expand": "Observations($orderby=phenomenonTime desc;$top=1)",
            "$filter": f"st_within(Thing/Locations/location, geography'POINT ({loc})')"
        }
        data_content = json.loads(requests.get(url, params=pa).text)
        infos = data_content['value']
        bulk = cls._get_collection().initialize_ordered_bulk_op()


        for info in infos:
            obs = [Observation(**i).to_mongo() for i in info.pop('Observations')]
            ci_datastream_model = cls(**info)
            ci_datastream_model.station = station
            ci_datastream_model.Observations.append(obs)
            ci_datastream_model.Location = tuple(map(float, location.split(',')))
            # bulk.find({"_iot_selfLink": ci_datastream_model['_iot_selfLink']}).upsert().update_one({'$setOnInsert':{'Observations': obs}})
            bulk.find({ "_iot_selfLink": ci_datastream_model['_iot_selfLink'] }).upsert().replace_one(ci_datastream_model.to_mongo())
        try:
            bulk.execute()
        except BulkWriteError as bwe:
            logging.error(bwe.details)
            raise

        if '@iot.nextLink' in data_content:
            cls.insert_all(station, location, url=data_content['@iot.nextLink'])

        
        query = {
            'name__icontains': 'NOW',
            'Location__near': tuple(map(float, location.split(',')))
        }

        return json.loads(cls.objects(**query).all().to_json())

    @classmethod
    def insert_all(cls, station:str, location:str, **kwargs):

        url = kwargs.get('url', f'https://sta.ci.taiwan.gov.tw/{station}/v1.0/Datastreams')
        loc = location.replace(',',' ')
        pa = {
            "$expand": "Observations($orderby=phenomenonTime desc;$top=1)",
            # "$filter": "st_within(Thing/Locations/location, geography'POINT (121.4946 24.7783)')"
            "$filter": f"st_within(Thing/Locations/location, geography'POINT ({loc})')"
        }
        data_content = json.loads(requests.get(url, params=pa).text)
        infos = data_content['value']
        bulk = cls._get_collection().initialize_ordered_bulk_op()

        for info in infos:
            # obs = [Observation(**i) for i in info.pop('Observations')]
            obs = [Observation(**i).to_mongo() for i in info.pop('Observations')]
            ci_datastream_model = cls(**info)
            ci_datastream_model.station = station
            # ci_datastream_model.Observations.append(obs)
            ci_datastream_model.Location = tuple(map(float, location.split(',')))
            bulk.find({"_iot_selfLink": ci_datastream_model['_iot_selfLink']}).upsert().update_one({'$setOnInsert':{'Observations': obs}})
        try:
            bulk.execute()
        except BulkWriteError as bwe:
            logging.error(bwe.details)
            raise

        if '@iot.nextLink' in data_content:
            cls.insert_all(station, location, url=data_content['@iot.nextLink'])
        return json.loads(cls.objects.all().to_json())

    @classmethod
    def insert(cls, station:str, location:str, **kwargs):

        url = kwargs.get('url', f'https://sta.ci.taiwan.gov.tw/{station}/v1.0/Datastreams')
        loc = location.replace(',',' ')
        pa = {
            "$expand": "Observations($orderby=phenomenonTime desc;$top=1)",
            "$filter": f"st_within(Thing/Locations/location, geography'POINT ({loc})')"
        }
        data_content = json.loads(requests.get(url, params=pa).text)
        infos = data_content['value']
        bulk = cls._get_collection().initialize_ordered_bulk_op()

        for info in infos:
            obs = [Observation(**i) for i in info.pop('Observations')]
            # obs = [Observation(**i).to_mongo() for i in info.pop('Observations')]
            ci_datastream_model = cls(**info)
            ci_datastream_model.station = station
            ci_datastream_model.Observations.append(obs)
            ci_datastream_model.Location = tuple(map(float, location.split(',')))
            ci_datastream_model.save()

        if '@iot.nextLink' in data_content:
            cls.insert_all(station, location, url=data_content['@iot.nextLink'])
        return json.loads(cls.objects.all().to_json())

    @classmethod
    def get(cls, args:dict):
        raw_query = {
            'Name': args['Name'], # ELEV, RAIN, MIN_10, HOUR_3, HOUR_6, HOUR_12, HOUR_24, NOW
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
    
class BaseDataTables:
    
    def __init__(self, request, columns, collection):
        
        self.columns = columns
        self.collection = collection
        # values specified by the datatable for filtering, sorting, paging
        self.request_values = request.values
        # results from the db
        self.result_data = None
        # total in the table after filtering
        self.cardinality_filtered = 0
        # total in the table unfiltered
        self.cadinality = 0
        self.run_queries()
    
    def output_result(self):
        
        output = {}
        # output['sEcho'] = str(int(self.request_values['sEcho']))
        # output['iTotalRecords'] = str(self.cardinality)
        # output['iTotalDisplayRecords'] = str(self.cardinality_filtered)
        aaData_rows = []
        for row in self.result_data:
            aaData_row = []
            for i in range(len(self.columns)):
                print(row, self.columns, self.columns[i])
                aaData_row.append(str(row[ self.columns[i] ]).replace('"','\\"'))
            aaData_rows.append(aaData_row)
        output['aaData'] = aaData_rows
        return output
    
    def run_queries(self):
        
         self.result_data = self.collection
         self.cardinality_filtered = len(self.result_data)
         self.cardinality = len(self.result_data)

columns = [ 'column_1', 'column_2', 'column_3', 'column_4']

# signals.pre_init.connect(Observation.pre_init, sender=Observation)