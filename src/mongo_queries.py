from pymongo import MongoClient

host = "174.138.13.47"
username = "Gsfbretsd"
password = "5erfFSTYUfnd"
db_name = "adressa_ofc"
db = MongoClient("mongodb://" + username + ':' + password + '@' + host + '/' + db_name)[db_name]


def create_article_profiles() -> list:
    profiles = []
    for article in db.articles.find():
        keyword = []
        for profile in article["profiles"]:
            keyword.append(profile["item"])
        profiles.append(keyword)
    return profiles


def create_user_profile(user_id) -> list:
    profiles = []
    events = db.user_profiles.find_one({"_id": user_id})["events"]
    visited_articles = list(map(lambda event: event["articleId"], events))
    for article_id in visited_articles:
        article = db.articles.find_one({"_id": article_id})
        for profile in article["profiles"]:
            profiles.append(profile["item"])
    return profiles
