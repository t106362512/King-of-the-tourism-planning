from flask import Flask
from flask_restful import Api
from flask_mongoengine import MongoEngine
from flask_bootstrap import Bootstrap
from .api.ScenicSpot import ScenicSpot
from .api.STAIOT import STALoc
from .views.demo import demo
import os

db = MongoEngine()

def create_app(config_name='development'):

    app = Flask(__name__)
    app.config["MONGODB_SETTINGS"] = {'DB': os.getenv('MONGODB_DB'), 'host': os.getenv('MONGODB_CONNECTIONSTRING')}
    api = Api(app)
    db.init_app(app)
    # bootstrap = Bootstrap(app)
    api.add_resource(ScenicSpot, '/api/scenice')
    api.add_resource(STALoc, '/api/location')
    # app.add_url_rule()
    app.register_blueprint(demo, url_prefix='/site')

    return app