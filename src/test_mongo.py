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
import numpy as np
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.similarities import MatrixSimilarity

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
counter = 0
keywords = []
article_map = {}

for article in articles.find():
    if article["keywords"] is not None:
        article_map[counter] = article["_id"]
        keywords.append(article["keywords"])
        counter += 1

dictionary = Dictionary(keywords)
corpus = list(map(lambda doc: dictionary.doc2bow(doc), keywords))
tfidf_model = TfidfModel(corpus)
tfidf_corpus = list(map(lambda c: tfidf_model[c], corpus))
tfidf_similarity = MatrixSimilarity(tfidf_corpus)

query_corpus = dictionary.doc2bow(['årets trønder', 'bybrann'])
query_tfidf = tfidf_model[query_corpus]
print(query_tfidf)

similarity = enumerate(tfidf_similarity[query_tfidf])
query_result = sorted(similarity, key=lambda kv: -kv[1])[:5]

results = list(map(lambda result: article_map[result[0]], query_result))
for result in results:
    pprint(articles.find_one({"_id": result})["title"])

#pprint(tdif_similarity)
#print(corpus[6])

#pprint(keywords)


#    for profile in article["profiles"]:
#        countInCollection[(profile["item"])] += 1
#        break
#    break

#N = articles.count()
#for key in countInCollection:
#    idf[key] = math.log2(N / countInCollection[key])




