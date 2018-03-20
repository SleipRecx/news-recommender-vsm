from pprint import pprint
from typing import Tuple, Dict
from pymongo import MongoClient
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.similarities import MatrixSimilarity


def mongo_connect(host, username, password, db_name):
    return MongoClient("mongodb://" + username + ':' + password + '@' + host + '/' + db_name)[db_name]


def create_article_profiles(db) -> Tuple[list, Dict]:
    index_article_map = {}
    current_index = 0
    profiles = []
    for article in db.articles.find():
        keyword = []
        index_article_map[current_index] = article["_id"]
        for profile in article["profiles"]:
            keyword.append(profile["item"])
        profiles.append(keyword)
        current_index += 1
    return profiles, index_article_map


def generate_user_profiles(db):
    result = []
    interactions = db.user_profiles.find()
    for i in range(10):
        interaction = interactions.next()
        visited_articles = list(map(lambda event: event["articleId"], interaction["events"]))
        profiles = []
        for article_id in visited_articles:
            article = db.articles.find_one({"_id": article_id})
            for profile in article["profiles"]:
                profiles.append(profile["item"])
        result.append(profiles)
    return result


if __name__ == '__main__':
    host = "167.99.45.145"
    username = "Gsfbretsd"
    password = "5erfFSTYUfnd"
    db_name = "adressa_ofc"
    db = mongo_connect(host, username, password, db_name)
    print("Connected")

    profiles, index_article_map = create_article_profiles(db)
    dictionary = Dictionary(profiles)
    corpus = list(map(lambda doc: dictionary.doc2bow(doc), profiles))
    tfidf_model = TfidfModel(corpus)
    tfidf_corpus = list(map(lambda c: tfidf_model[c], corpus))
    tfidf_similarity = MatrixSimilarity(tfidf_corpus)
    print("Model built")

    queries = generate_user_profiles(db)
    for query in queries:
        query_corpus = dictionary.doc2bow(query)
        query_tfidf = tfidf_model[query_corpus]
        similarity = enumerate(tfidf_similarity[query_tfidf])
        query_result = sorted(similarity, key=lambda kv: -kv[1])[:30]
        results = list(map(lambda result: index_article_map[result[0]], query_result))
        for result in results:
            pprint(db.articles.find_one({"_id": result})["title"])
        print("------------------------")

    while True:
        query = input("Query: ")
        query_corpus = dictionary.doc2bow(query.split())
        query_tfidf = tfidf_model[query_corpus]

        similarity = enumerate(tfidf_similarity[query_tfidf])

        query_result = sorted(similarity, key=lambda kv: -kv[1])[:5]

        results = list(map(lambda result: index_article_map[result[0]], query_result))

        for result in results:
            pprint(db.articles.find_one({"_id": result})["title"])
