from pprint import pprint
from model import VectorSpaceModel
from mongo_queries import create_article_profiles, create_user_profile, db
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
    average_precision = 1
    average_recall = 1
    recall_map = defaultdict(int)
    precision_map = defaultdict(int)

    n_predictions = 30
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
        results = model.query(query=user_profile, n_results=30)
        results = list(filter(lambda x: x not in read_ids, results))  # filters out already read articles
        articles = get_articles_from_query_result(results)
        recommended_ids = list(map(lambda x: x['_id'], articles))
        # pprint(list(map(lambda x: x['title'], articles)))
        print(i)
        for x in range(1, 31):
            rec2 = recommended_ids[:x]
            true_positives = len(set(rec2).intersection(set(test_read_ids)))
            false_positives = len(rec2) - true_positives
            false_negatives = len(test_read_ids) - true_positives

            precision = true_positives / (true_positives + false_positives)
            recall = true_positives / (true_positives + false_negatives)

            recall_map[x] += recall
            precision_map[x] += precision

            # print()
            # print('Precision:', precision * 100, '%')
            # print('Recall:', recall * 100, '%')
            # average_precision += precision
            # average_recall += recall

    for key in range(1, 31):
        precision_map[key] /= n_predictions
        recall_map[key] /= n_predictions
        print()
        print(key, "Precision:", precision_map[key])
        print(key, "Recall:", recall_map[key])
        print(key, "F-Measure:", 2 * (precision_map[key] * recall_map[key] / (precision_map[key] + recall_map[key])))

        # f_measure = 2 * (average_precision * average_recall / (average_precision + average_recall))
        # print('Average Precision:', average_precision * 100, '%')
        # print('Average Recall:', average_recall * 100, '%')
        # print('F-Measure:', f_measure)
