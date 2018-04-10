# Project: web-intelligens
# Created: 10.04.18 17:42
# Owner: Espen Meidell
from collections import defaultdict
from mongo_queries import db, get_n_most_popular


def create_most_popular():
    c_user = db.user_profiles.count()
    count = defaultdict(int)
    c = 0
    for user in db.user_profiles.find():
        print(c, "/", c_user)
        for event in user["events"]:
            count[event["articleId"]] += 1
        c += 1
    article_ids = list(count.keys())
    article_ids.sort(key=lambda x: count[x])
    most_pop = article_ids[len(article_ids) - 1000:]
    most_pop.reverse()
    for i in range(len(most_pop)):
        db.most_popular.insert({"_id": i, "articleId": most_pop[i]})


if __name__ == '__main__':
    get_n_most_popular(10)
