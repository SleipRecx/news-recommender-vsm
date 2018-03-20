# Project: web-intelligens
# Created: 09.03.18 13:41
# Owner: Espen Meidell


from pprint import pprint
from collections import defaultdict
from pymongo import MongoClient
from gensim.corpora import Dictionary
from gensim.models import TfidfModel, LsiModel
from gensim.similarities import MatrixSimilarity

client = MongoClient("mongodb://Gsfbretsd:5erfFSTYUfnd@167.99.45.145/adressa_ofc")
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


counter = 0
profiles = []
article_map = {}

for article in articles.find():
    keyword = []
    article_map[counter] = article["_id"]
    for profile in article["profiles"]:
        keyword.append(profile["item"])
    profiles.append(keyword)
    counter += 1

print("keywords made")
dictionary = Dictionary(profiles)
print("created dict")
corpus = list(map(lambda doc: dictionary.doc2bow(doc), profiles))
print("created corpus")
tfidf_model = TfidfModel(corpus)
print("created model")
tfidf_corpus = list(map(lambda c: tfidf_model[c], corpus))
print("created corpus2")
tfidf_similarity = MatrixSimilarity(tfidf_corpus)
print("gg wp")

query_corpus = dictionary.doc2bow(['ol', 'vm', "langrenn"])

query_tfidf = tfidf_model[query_corpus]

similarity = enumerate(tfidf_similarity[query_tfidf])

query_result = sorted(similarity, key=lambda kv: -kv[1])[:5]


results = list(map(lambda result: article_map[result[0]], query_result))
for result in results:
    pprint(articles.find_one({"_id": result})["title"])
