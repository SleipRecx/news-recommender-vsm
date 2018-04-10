import numpy as np
from sklearn.metrics import roc_auc_score
from src.model import VectorSpaceModel
from src.mongo_queries import db, create_user_profile, get_n_most_popular
import time
import os

n_users = 100
n_articles_2_rec = 10
threshold = 0.25


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
    n_articles = db.articles.find().count()

    recall_list = []
    precision_list = []
    arhr_list = []
    auc_list = []

    for i in range(n_users):
        print(i)
        current_user = user_profile_iterator.next()["_id"]

        user_profile = create_user_profile(current_user)
        read = db.user_profiles.find_one()["events"]
        read_ids = list(map(lambda x: x['articleId'], read))

        test_read = db.test_user_profiles.find_one({"_id": current_user})["events"]
        test_read_ids = list(map(lambda x: x['articleId'], test_read))

        query_results = model.query(query=user_profile, threshold=threshold)
        results = list(map(lambda x: x[0], query_results))
        results = list(filter(lambda x: x not in read_ids, results))  # filters out already read articles
        articles = get_articles_from_query_result(results)

        if len(articles) > int(n_articles_2_rec):
            articles = articles[:int(n_articles_2_rec)]
        if len(articles) < int(n_articles_2_rec):
            n_missing = int(n_articles_2_rec) - len(articles) + len(read_ids)
            most_popular = get_n_most_popular(n_missing)
            tmp_recommended_ids = list(map(lambda x: x['_id'], articles))
            for popular_article in most_popular:
                if popular_article['_id'] not in read_ids and popular_article['_id'] not in tmp_recommended_ids:
                    articles.append(popular_article)
                    if len(articles) == int(n_articles_2_rec):
                        break

        recommended_ids = list(map(lambda x: x['_id'], articles))

        true_positives = len(set(recommended_ids).intersection(set(test_read_ids)))
        false_positives = len(recommended_ids) - true_positives
        false_negatives = len(test_read_ids) - true_positives
        true_negatives = n_articles - true_positives - false_positives - false_negatives

        y_true = []
        y_score = []
        for article in db.articles.find():
            if article["_id"] in test_read_ids:
                y_true.append(1)
            else:
                y_true.append(0)
            if article["_id"] in recommended_ids:
                y_score.append(1)
            else:
                y_score.append(0)
        y_true = np.array(y_true)
        y_score = np.array(y_score)
        auc = roc_auc_score(y_true, y_score)

        try:
            precision = true_positives / (true_positives + false_positives)
        except ZeroDivisionError:
            precision = 0
        try:
            recall = true_positives / (true_positives + false_negatives)
        except ZeroDivisionError:
            recall = 0
        try:
            f_measure = 2 * (precision * recall / (precision + recall))
        except ZeroDivisionError:
            f_measure = 0

        arhr = sum(
            list(map(lambda x: 0 if x not in recommended_ids else 1 / (recommended_ids.index(x) + 1), test_read_ids)))

        recall_list.append(recall)
        precision_list.append(precision)
        arhr_list.append(arhr)
        auc_list.append(auc)

    global_precision = sum(precision_list) / len(precision_list)
    global_recall = sum(recall_list) / len(recall_list)
    global_f_measure = 2 * (global_precision * global_recall / (global_precision + global_recall))
    global_arhr = sum(arhr_list) / len(arhr_list)
    global_auc = sum(auc_list) / len(auc_list)

    print("Global Precision:", global_precision)
    print("Global Recall:", global_recall)
    print("Global F-Measure:", global_f_measure)
    print("Global ARHR:", global_arhr)
    print("Global AUC", global_auc)
