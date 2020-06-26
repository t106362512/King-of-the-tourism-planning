from flask import Flask
from flask_restful import Api
from flask_caching import Cache
from flask_mongoengine import MongoEngine
from flask_bootstrap import Bootstrap
from .api.ScenicSpot import ScenicSpot
from .api.STAIOT import STALoc
from .views.demo import demo
from .views.datatable import datable
import os

db = MongoEngine()
cache = Cache(config={'CACHE_TYPE': 'simple'})

def create_app():

    app = Flask(__name__)
    app.config["MONGODB_SETTINGS"] = {'DB': os.getenv('MONGODB_DB'), 'host': os.getenv('MONGODB_CONNECTIONSTRING')}
    app.jinja_env.globals['MAPBOX_API_KEY'] = os.getenv('MAPBOX_API_KEY')
    api = Api(app)
    db.init_app(app)
    cache.init_app(app)
    api.add_resource(ScenicSpot, '/api/scenice', endpoint='api.scenice') # end point for jinja2 url_for using
    api.add_resource(STALoc, '/api/location', endpoint='api.stalocation')
    app.register_blueprint(demo, url_prefix='/site')
    app.register_blueprint(datable)

    return app