from flask import Flask
from flask_restful import Api
from flask_mongoengine import MongoEngine
from resources.ScenicSpot import ScenicSpot_resource
import os

db = MongoEngine()

def create_app(config_name='development'):

    app = Flask(__name__)
    app.config["MONGODB_SETTINGS"] = {'DB': os.getenv('MONGODB_DB'), 'host': os.getenv('MONGODB_CONNECTIONSTRING')}
    api = Api(app)
    db.init_app(app)
    api.add_resource(ScenicSpot_resource, '/scenice')
    return app