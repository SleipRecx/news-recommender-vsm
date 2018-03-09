# Project: web-intelligens
# Created: 09.03.18 13:41
# Owner: Espen Meidell
import json
import pymongo
from pymongo import MongoClient

# mongodb://<dbuser>:<dbpassword>@ds261088.mlab.com:61088/adressa-articles

client = MongoClient("mongodb://gutta:gutta@ds261088.mlab.com:61088/adressa-articles")

db = client["adressa-articles"]
articles = db.articles

with open("articles.json") as file:
    json = json.loads(file.read())
    for key in json:
        articles.insert_one(json[key])