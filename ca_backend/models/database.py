import pymongo

class Database():

    @classmethod
    def initialize(cls, *args, **kwargs):
        # client = pymongo.MongoClient("mongodb://localhost:27017/test_db")
        client = pymongo.MongoClient('mongodb+srv://ccw:cvber234@cluster0-degz6.gcp.mongodb.net/test?retryWrites=true&w=majority')
        cls.database = client.get_default_database()

    @classmethod
    def save_to_db(cls, data):
        return cls.database.stores.insert_one(data)    

    @classmethod
    def load_from_db(cls, query):
        return cls.database.stores.find(query)