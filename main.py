from pprint import pprint
from model import VectorSpaceModel
from mongo_queries import create_article_profiles, create_user_profile, db
import os

if __name__ == '__main__':
    model_path = os.getcwd() + '/model'

    model = VectorSpaceModel()
    # profiles, index_article_map = create_article_profiles(db)
    # model.build(profiles, profile_index_map=index_article_map)
    # model.save(path=model_path)

    user_profile = create_user_profile(db.user_profiles.find_one()["_id"])
    model.load(path=model_path)
    query = ['sport', 'fotball', 'mål']
    results = model.query(query=user_profile, n_results=100)
    for result in results:
        pprint(db.articles.find_one({"_id": result})['title'])
