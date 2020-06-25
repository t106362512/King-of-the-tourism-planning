from pymongo import MongoClient
import random

client = MongoClient(
    'mongodb+srv://admin:admin@scenicspotinfo-sh83l.gcp.mongodb.net/test?retryWrites=true&w=majority')

# print(client.database_names())
db = client['test']

# print(db.collection_names())
collection = db['scenic_spot_info']

target_list = list()

num1 = random.randrange(1, collection.count()-10)
print('num1 = {}'.format(num1))
# documents = collection.find()[random.randrange(collection.count())]
documents = collection.find()[num1:num1+10]
for document in documents:
    local_dict = dict()
    print('Id = {}, Name = {}, Local = {}'.format(
        document['Id'], document['Name'], document['Location']))
    local_dict['Id'] = document['Id']
    local_dict['Name'] = document['Name']
    local_dict['Location'] = document['Location']

    target_list.append(local_dict)

print(target_list)
