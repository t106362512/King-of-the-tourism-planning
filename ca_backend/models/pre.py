from marshmallow import Schema, fields, pre_dump, pre_load, post_dump, post_load, INCLUDE, RAISE, EXCLUDE


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

