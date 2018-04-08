from pprint import pprint
from src.model import VectorSpaceModel
from src.mongo_queries import create_article_profiles, create_user_profile, db
from collections import defaultdict
import os
import time


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

    user_profile_iterator = db.test_user_profiles.find()
    n_test_articles = db.test_articles.find().count()

    recall_list = []
    precision_list = []
    fpr_list = []

    average_recall = 0
    average_precision = 0

    n_predictions = 1000
    for i in range(n_predictions):
        current_user = user_profile_iterator.next()["_id"]
        user_profile = create_user_profile(current_user)
        read = db.user_profiles.find_one()["events"]
        read_ids = list(map(lambda x: x['articleId'], read))

        # print("Train")
        # for read_id in read_ids:
        #     pprint(db.articles.find_one({"_id": read_id})['title'])
        # print()

        test_read = db.test_user_profiles.find_one({"_id": current_user})["events"]
        test_read_ids = list(map(lambda x: x['articleId'], test_read))
        #
        # print("Test")
        # for read_id in test_read_ids:
        #     pprint(db.articles.find_one({"_id": read_id})['title'])
        # print()

        start = time.time()
        results = model.query(query=user_profile, n_results=3)
        results = list(filter(lambda x: x not in read_ids, results))  # filters out already read articles
        articles = get_articles_from_query_result(results)
        recommended_ids = list(map(lambda x: x['_id'], articles))
        # pprint(list(map(lambda x: x['title'], articles)))
        print("User:", i + 1)

        true_positives = len(set(recommended_ids).intersection(set(test_read_ids)))
        false_positives = len(recommended_ids) - true_positives
        false_negatives = len(test_read_ids) - true_positives
        true_negatives = n_test_articles - (false_negatives + true_positives) - false_positives

        false_positives_rate = false_positives / (false_positives + true_negatives)
        precision = true_positives / (true_positives + false_positives)
        recall = true_positives / (true_positives + false_negatives)

        recall_list.append(recall)
        precision_list.append(precision)
        fpr_list.append(false_positives_rate)

    average_precision = sum(precision_list) / len(precision_list)
    average_recall = sum(recall_list) / len(recall_list)

    print("Precision:", average_precision)
    print("Recall:", average_recall)
    print("F-Measure:", 2 * (average_precision * average_recall / (average_precision + average_recall)))
    print("fpr")
    pprint(fpr_list)
    print("recall")
    pprint(recall_list)
