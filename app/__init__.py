from flask import Flask
from flask_restful import Api
from flask_caching import Cache
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from flask_bootstrap import Bootstrap
from app.api.ScenicSpot import ScenicSpot
from app.api.STAIOT import STALoc
from app.api.RoutePlanning import RoutePlanning
from app.views.demo import demo
from app.views.datatable import datable
from app.views.RoutePlanning import RoutePlanning_bp
# from flask_marshmallow import Marshmallow
import os

db = MongoEngine()
# ma = Marshmallow()
cache = Cache(config={'CACHE_TYPE': 'simple'})

def create_app(config_name='development'):
    # pylint: disable=no-member

    app = Flask(__name__)
    app.config["MONGODB_SETTINGS"] = {'DB': os.getenv('MONGODB_DB'), 'host': os.getenv('MONGODB_CONNECTIONSTRING')}
    app.jinja_env.globals['MAPBOX_API_KEY'] = os.getenv('MAPBOX_API_KEY')
    api = Api(app)
    db.init_app(app)
    cache.init_app(app)
    # ma.init_app(app)
    api.add_resource(ScenicSpot, '/api/scenice', endpoint='api.scenice') # end point for jinja2 url_for using
    api.add_resource(STALoc, '/api/location', endpoint='api.stalocation')
    api.add_resource(RoutePlanning, '/api/RoutePlanning', endpoint='api.RoutePlanning')
    app.register_blueprint(demo, url_prefix='/site')
    app.register_blueprint(RoutePlanning_bp, url_prefix='/RoutePlanning')
    app.register_blueprint(datable, url_prefix='/')
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    return app