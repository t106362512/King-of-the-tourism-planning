
# from __future__ import barry_as_FLUFL
# from .database import Database
# from .model import *

# __all__ = ['Location', 'Observation', 'Thing', 'Datastream', 'FullDatastream', 'Database']
# __version__ = '0.1'
# __author__ = 'CCW'

from flask_mongoengine import MongoEngine
from flask_pymongo import PyMongo

db = MongoEngine()
pymdb = PyMongo()