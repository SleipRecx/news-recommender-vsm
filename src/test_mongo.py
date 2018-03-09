# Project: web-intelligens
# Created: 09.03.18 13:41
# Owner: Espen Meidell
import json
import pymongo
from pprint import pprint
from pymongo import MongoClient


client = MongoClient("mongodb://admin:gutta123@138.68.107.82:27017")
# client = MongoClient("mongodb://gutta:gutta@ds261088.mlab.com:61088/adressa-articles")

db = client["adressa-articles"]
print("Connected")

articles = db.articles
user_profiles = db.user_profiles

print("Number of articles:", articles.count())

print("Number of users:", user_profiles.count())

print("User with most reads:", user_profiles.find().sort([("", pymongo.ASCENDING)]).next())