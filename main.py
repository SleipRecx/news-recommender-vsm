from pprint import pprint
from src.model import VectorSpaceModel
from src.mongo_queries import create_article_profiles, create_user_profile, db
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
    n_articles = db.articles.find().count()

    recall_list = []
    precision_list = []
    arhr_list = []
    fpr_list = []

    n_predictions = 100
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
        query_results = model.query(query=user_profile, threshold=0.5)
        if len(query_results) == 0:
            precision = 1
            recall = 0
            false_positives_rate = 0
            arhr = 0
        else:
            results = list(map(lambda x: x[0], query_results))
            results = list(filter(lambda x: x not in read_ids, results))  # filters out already read articles
            articles = get_articles_from_query_result(results)
            recommended_ids = list(map(lambda x: x['_id'], articles))

            pprint(list(map(lambda x: x['title'], articles)))
            print("User:", i + 1)

            true_positives = len(set(recommended_ids).intersection(set(test_read_ids)))
            false_positives = len(recommended_ids) - true_positives
            false_negatives = len(test_read_ids) - true_positives
            true_negatives = n_articles - false_negatives - true_positives - false_positives

            false_positives_rate = false_positives / (false_positives + true_negatives)
            precision = true_positives / (true_positives + false_positives)
            recall = true_positives / (true_positives + false_negatives)
            arhr = sum(
                list(map(lambda x: 0 if x not in recommended_ids else 1 / (recommended_ids.index(x) + 1), test_read_ids)))

        recall_list.append(recall)
        precision_list.append(precision)
        arhr_list.append(arhr)
        fpr_list.append(false_positives_rate)

    global_precision = sum(precision_list) / len(precision_list)
    global_recall = sum(recall_list) / len(recall_list)
    global_f_measure = 2 * (global_precision * global_recall / (global_precision + global_recall))
    global_arhr = sum(arhr_list) / len(arhr_list)
    global_fpr = sum(fpr_list) / len(fpr_list)

    print("Global Precision:", global_precision)
    print("Global Recall:", global_recall)
    print("Global F-Measure:", global_f_measure)
    print("Global ARHR:", global_arhr)
    print("Gloabl FPR:", global_fpr)

