from flask import Flask
from flask_restful import Api
from flask_caching import Cache
from flask_mongoengine import MongoEngine
from flask_cors import CORS
import os

me = MongoEngine()
cache = Cache()

def create_app(config_name='development'):
    # pylint: disable=no-member

    from backend.api.ScenicSpot import ScenicSpot
    from backend.api.STAIOT import STALoc
    from backend.api.RoutePlanning import RoutePlanning
    # from backend.api.datatable_server_side.ScenicSpot import ScenicSpot
    from backend.views.demo import demo
    from backend.views.datatable import datable
    from backend.views.RoutePlanning import RoutePlanning_bp

    app = Flask(__name__)
    app.config["MONGODB_SETTINGS"] = {'DB': os.getenv('MONGODB_DB'), 'host': os.getenv('MONGODB_CONNECTIONSTRING')}
    app.jinja_env.globals['MAPBOX_API_KEY'] = os.getenv('MAPBOX_API_KEY')
    app.jinja_env.globals['GOOGLE_PLACES_API_KEY'] = os.getenv('GOOGLE_PLACES_API_KEY')
    api = Api(app)
    me.init_app(app)
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})
    api.add_resource(ScenicSpot, '/api/scenice', endpoint='api.scenice') # end point for jinja2 url_for using
    api.add_resource(STALoc, '/api/location', endpoint='api.stalocation')
    api.add_resource(RoutePlanning, '/api/RoutePlanning', endpoint='api.RoutePlanning')
    app.register_blueprint(demo, url_prefix='/site')
    app.register_blueprint(RoutePlanning_bp, url_prefix='/RoutePlanning')
    app.register_blueprint(datable, url_prefix='/')
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    return app