import json
import pymongo
from pymongo import MongoClient

# mongodb://<dbuser>:<dbpassword>@ds261088.mlab.com:61088/adressa-articles

client = MongoClient("mongodb://Gsfbretsd:5erfFSTYUfnd@167.99.45.145/adressa_ofc")
# client = MongoClient("mongodb://gutta:gutta@ds261088.mlab.com:61088/adressa-articles")

print(client.server_info())

db = client["adressa_ofc"]
articles = db.articles
user_profiles = db.user_profiles
test_articles = db.test_articles
test_user_profiles = db.test_user_profiles

# with open("articles.json") as file:
#     json = json.loads(file.read())
#     print(len(json))
#     articles.insert_many(json)
#     print("Done inserting")

# with open("users.json") as file:
#     json = json.loads(file.read())
#     print(len(json))
#     user_profiles.insert_many(json)
#     print("Done inserting")


# with open("test_users.json") as file:
#     json = json.loads(file.read())
#     print(len(json))
#     test_user_profiles.insert_many(json)
#     print("Done inserting")


# with open("test_articles.json") as file:
#     json = json.loads(file.read())
#     print(len(json))
#     test_articles.insert_many(json)
#     print("Done inserting")