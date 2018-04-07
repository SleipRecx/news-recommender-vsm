from typing import Tuple, Dict
from pymongo import MongoClient

host = "167.99.45.145"
username = "Gsfbretsd"
password = "5erfFSTYUfnd"
db_name = "adressa_ofc"
db = MongoClient("mongodb://" + username + ':' + password + '@' + host + '/' + db_name)[db_name]


def create_article_profiles() -> Tuple[list, Dict]:
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


def create_user_profile(user_id) -> list:
    profiles = []
    events = db.user_profiles.find_one({"_id": user_id})["events"]
    visited_articles = list(map(lambda event: event["articleId"], events))
    for article_id in visited_articles:
        article = db.articles.find_one({"_id": article_id})
        for profile in article["profiles"]:
            profiles.append(profile["item"])
    return profiles


def generate_user_profiles() -> Tuple[list, dict]:
    user_index_map = {}
    result = []
    interactions = db.user_profiles.find()
    for interaction, i in interactions:
        user_index_map[i] = interaction["_id"]
        visited_articles = list(map(lambda event: event["articleId"], interaction["events"]))
        profiles = []
        for article_id in visited_articles:
            article = db.articles.find_one({"_id": article_id})
            for profile in article["profiles"]:
                profiles.append(profile["item"])
        result.append(profiles)
    return result, user_index_map

