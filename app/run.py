import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Flask, make_response
from flask.json import JSONEncoder

from flask_restful import fields, marshal_with, Api, Resource

from marshmallow import Schema, fields, pre_dump, pre_load, post_dump, RAISE

import requests 
import json

api = Api()
app = Flask(__name__)
api.init_app(app)




class WaterResource(Resource):


    ep = 'https://sta.ci.taiwan.gov.tw/STA_AirQuality_v2/v1.0/Datastreams(11)/Thing'
    r = requests.get(url=ep)

    _resource_fields = {
            'name': fields.String,
            'description': fields.String,
            # 'date_updated': fields.DateTime(dt_format='rfc822')
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(self, *args, **kwargs)
        
    @marshal_with(_resource_fields, envelope='resource')
    def get(self, *args, **kwargs):
        return 

    def output_json(self, data, code, headers=None):
        """Makes a Flask response with a JSON encoded body"""

        resp = make_response(json.dumps(data), code)
        resp.headers.extend(headers or {})
        return resp

class STS(Schema):

    class Meta:
            unknown = True
    name=fields.Str()
    description=fields.Str()
    # properties=fields.Nested()

ep = 'https://sta.ci.taiwan.gov.tw/STA_AirQuality_v2/v1.0/Datastreams(11)/Thing'
r = requests.get(url=ep).text
a = STS().loads(r)
print(a)