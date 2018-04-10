from model import VectorSpaceModel
from mongo_queries import db, create_user_profile, get_n_most_popular
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

    user_profile_iterator = db.test_user_profiles.find()

    while True:
        input("Continue...")
        print()
        current_user = user_profile_iterator.next()["_id"]
        user_json = db.user_profiles.find_one({"_id": current_user})
        city = user_json['city']
        print("Current user:", current_user, "from", city)
        print()

        user_profile = create_user_profile(current_user)
        read = db.user_profiles.find_one()["events"]
        read_ids = list(map(lambda x: x['articleId'], read))

        print("Articles read by user:")
        print("-" * 50)
        for read_id in read_ids:
            print(db.articles.find_one({"_id": read_id})['title'])
        print()

        test_read = db.test_user_profiles.find_one({"_id": current_user})["events"]
        test_read_ids = list(map(lambda x: x['articleId'], test_read))

        print("Articles also read by user, NOT known by our model:")
        print("-" * 50)
        for read_id in test_read_ids:
            print(db.articles.find_one({"_id": read_id})['title'])
        print()

        n_articles_2_rec = input("How many articles to recommend? ")

        query_results = model.query(query=user_profile, threshold=0.01)

        if n_articles_2_rec != 'n' and n_articles_2_rec != 'N':
            if len(query_results) > int(n_articles_2_rec):
                query_results = query_results[:int(n_articles_2_rec)]

        results = list(map(lambda x: x[0], query_results))
        results = list(filter(lambda x: x not in read_ids, results))  # filters out already read articles
        articles = get_articles_from_query_result(results)

        if n_articles_2_rec != 'n' and n_articles_2_rec != 'N':
            if len(articles) < int(n_articles_2_rec):
                n_missing = int(n_articles_2_rec) - len(articles) + len(read_ids)
                most_popular = get_n_most_popular(n_missing)
                tmp_recommended_ids = list(map(lambda x: x['_id'], articles))
                for popular_article in most_popular:
                    if popular_article['_id'] not in read_ids and popular_article['_id'] not in tmp_recommended_ids:
                        articles.append(popular_article)
                        if len(articles) == int(n_articles_2_rec):
                            break

        article_titles = list(map(lambda x: x['title'], articles))
        print("Our model recommends the following articles:")
        print("-" * 50)
        for i in range(len(article_titles)):
            print(i + 1, article_titles[i])
        print()

        recommended_ids = list(map(lambda x: x['_id'], articles))
        true_positives = len(set(recommended_ids).intersection(set(test_read_ids)))
        false_positives = len(recommended_ids) - true_positives
        false_negatives = len(test_read_ids) - true_positives
        precision = true_positives / (true_positives + false_positives)
        recall = true_positives / (true_positives + false_negatives)
        f_measure = 2 * (precision * recall / (precision + recall))
        arhr = sum(
            list(map(lambda x: 0 if x not in recommended_ids else 1 / (recommended_ids.index(x) + 1), test_read_ids)))

        print("Precision:", "%.2f" % (precision * 100) + '%')
        print("Recall:", "%.2f" % (recall * 100) + '%')
        print("F1-Score:", "%.2f" % f_measure)
        print("ARHR:", "%.2f" % arhr)
        print()
