from flask import Flask
from flask_restful import Api

db = SQLAlchemy()

jwt = JWT(None, UserModel.authenticate, UserModel.identity)


def create_app(config_name='development'):

    app = Flask(__name__)
    api = Api(app)
    app.config["MONGODB_SETTINGS"] = {'DB': "test", "host":'mongodb+srv://ccw:cvber234@cluster0-degz6.gcp.mongodb.net/test?retryWrites=true&w=majority'}
    db.init_app(app)
    
    api.add_resource(ScenicSpot_resource, '/scenice')

    return app