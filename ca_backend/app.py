from flask import Flask
from flask_restful import Resource, Api
from models import db
from models.database import Database
from resources.ScenicSpot import ScenicSpot_resource
from . import create_app
# from api.sta_iot import STA
import os

if __name__ == "__main__":

    # app.config['MONGODB_DB'] = os.getenv('MONGODB_DB')
    # app.config['MONGODB_HOST'] = os.getenv('MONGODB_HOST')
    # app.config['MONGODB_USERNAME'] = os.getenv('MONGODB_USERNAME')
    # app.config['MONGODB_PASSWORD'] = os.getenv('MONGODB_PASSWORD')
    # app.config["MONGODB_SETTINGS"] = {'DB': "test", "host":'mongodb+srv://ccw:cvber234@cluster0-degz6.gcp.mongodb.net/test?retryWrites=true&w=majority'}
    # app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    # app.config['MONGO_HOST'] = os.getenv('MONGO_HOST')
    # app.config['MONGO_DBNAME'] = os.getenv('MONGO_DBNAME')
    # app.config['MONGO_USERNAME'] = os.getenv('MONGO_USERNAME')
    # app.config['MONGO_PASSWORD'] = os.getenv('MONGO_PASSWORD')
    # pymdb.init_app(app)
    # Database.initialize(os.getenv('MONGO_URI'))
    # api.add_resource(STA, '/sta/<string:url>')

    app = create_app()

    app.run()