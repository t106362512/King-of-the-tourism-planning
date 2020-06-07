from flask_restful import Resource, request
from ..models.database import Database
from ..models.model import FullDatastream
import requests

class STA(Resource):
    
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass

    def put(self, url, params, *args, **kwargs):
        content = requests.get(url, params, **kwargs).text
        result = FullDatastream().loads(content).data
        Database.save_to_db(result)
        return result

    def delete(self, *args, **kwargs):
        pass