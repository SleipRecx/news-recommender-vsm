# Project: web-intelligens
# Created: 09.03.18 13:41
# Owner: Espen Meidell
import json
import pymongo
from pymongo import MongoClient

# mongodb://<dbuser>:<dbpassword>@ds261088.mlab.com:61088/adressa-articles

client = MongoClient("mongodb://admin:gutta123@138.68.107.82:27017")
# client = MongoClient("mongodb://gutta:gutta@ds261088.mlab.com:61088/adressa-articles")

print(client.server_info())

db = client["adressa-articles"]
articles = db.articles
user_profiles = db.user_profiles

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