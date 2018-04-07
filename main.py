from pprint import pprint
from model import VectorSpaceModel
from mongo_queries import create_article_profiles, create_user_profile, db
import os


def get_articles_from_query_result(result):
    articles = list(map(lambda x: list(db.articles.find().limit(1).skip(x))[0], result))
    return articles


if __name__ == '__main__':
    model_path = os.getcwd() + '/model'

    model = VectorSpaceModel()
    model.load(path=model_path)
    # profiles = create_article_profiles()
    # model.build(profiles)
    # model.save(path=model_path)

    user_profile_iterator = db.test_user_profiles.find()

    for i in range(0):
        user_profile_iterator.next()

    current_user = user_profile_iterator.next()["_id"]

    user_profile = create_user_profile(current_user)
    read = db.user_profiles.find_one()["events"]
    read_ids = list(map(lambda x: x['articleId'], read))

    print("Train")
    for id in read_ids:
        pprint(db.articles.find_one({"_id": id})['title'])
    print()

    test_read = db.test_user_profiles.find_one({"_id": current_user})["events"]
    test_read_ids = list(map(lambda x: x['articleId'], test_read))

    print("Test")
    for id in test_read_ids:
        pprint(db.articles.find_one({"_id": id})['title'])
    print()

    results = model.query(query=user_profile, n_results=10)
    results = list(filter(lambda x: x not in read_ids, results))
    articles = get_articles_from_query_result(results)
    pprint(list(map(lambda x: x['title'], articles)))
