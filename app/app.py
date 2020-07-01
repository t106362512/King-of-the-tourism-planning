from flask import Flask
from flask_restful import Resource, Api
from app.models import db
from app.models.database import Database
from app import create_app
# from api.sta_iot import STA
import os




if __name__ == "__main__":

    app = create_app()
    app.run()