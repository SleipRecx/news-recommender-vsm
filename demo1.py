from model import VectorSpaceModel
from mongo_queries import db
import time
import os


def get_articles_from_query_result(result):
    articles = list(map(lambda x: list(db.articles.find().limit(1).skip(x))[0], result))
    return articles


if __name__ == '__main__':
    start = time.time()
    model_path = os.getcwd() + '/model'

    model = VectorSpaceModel()
    model.load(path=model_path)
    # profiles = create_article_profiles()
    # model.build(profiles)
    # model.save(path=model_path)
    print("Building time:", time.time() - start)

    while True:
        query = input("Query: ").split()
        query_results = model.query(query=query, threshold=0.1)
        results = list(map(lambda x: x[0], query_results))
        articles = get_articles_from_query_result(results)
        for i in range(0, len(articles)):
            print(i + 1, articles[i]['title'])

