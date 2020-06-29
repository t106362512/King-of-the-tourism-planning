from flask import Flask
from flask_restful import Resource, Api
from .models import db
from .models.database import Database
from . import create_app
# from api.sta_iot import STA
import os

if __name__ == "__main__":

    app = create_app()

    app.run(debug=True)