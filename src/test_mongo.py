# Project: web-intelligens
# Created: 09.03.18 13:41
# Owner: Espen Meidell
import json
import pymongo
from pprint import pprint
import math

from bson import SON
from collections import defaultdict
from pymongo import MongoClient


client = MongoClient("mongodb://Gsfbretsd:5erfFSTYUfnd@167.99.45.145/adressa_ofc")
# client = MongoClient("mongodb://gutta:gutta@ds261088.mlab.com:61088/adressa-articles")

db = client["adressa_ofc"]
print("Connected")

articles = db.articles
user_profiles = db.user_profiles

print("Number of articles:", articles.count())

print("Number of users:", user_profiles.count())

# # Find information for one users events
# events = user_profiles.find_one({"_id": "cx:2fs9x8i7jvcjyckoxqfa6l4lw:3rr1gvpcbzx8w"})["events"]
#
# article_profile_items = defaultdict(int)
#
# for event in events:
#     for profile in articles.find_one({"_id": event["articleId"]})["profiles"]:
#         article_profile_items[(profile["item"])] += 1
#
# pprint(article_profile_items)

countInCollection = defaultdict(int)
idf = {}
for article in articles.find():
    for profile in article["profiles"]:
        countInCollection[(profile["item"])] += 1

N = articles.count()
for key in countInCollection:
    idf[key] = math.log2(N / countInCollection[key])

