import json
from collections import defaultdict
from typing import Dict


def save_dict_as_json(filename: str, out_dict: Dict):
    out_list = []
    for _, item in out_dict.items():
        out_list.append(item)
    with open(filename + '.json', 'w') as out_file:
        out_file.write(json.dumps(out_list, indent=2, ensure_ascii=False))


def create_article_dict(filename: str, output: Dict = None) -> Dict:
    if output is None:
        output = {}
    with open(filename, 'r') as fil:
        for line in fil:
            article = json.loads(line.strip())
            if 'id' in article:
                key = article['id']
                if key not in output:
                    obj = dict(_id=article['id'],
                               title=article['title'],
                               url=article['url'],
                               pluss='pluss' in article['url'],
                               authors=article['author'] if 'author' in article else None,
                               keywords=article['keywords'].split(',') if 'keywords' in article else None,
                               categories=article['category1'].split('|') if 'category1' in article else None,
                               publishTime=article['publishTime'] if 'publishTime' in article else None,
                               profiles=article['profile'][3:])
                    output[key] = obj
    return output


def create_user_dict(filename: str, output: Dict = None) -> Dict:
    if output is None:
        output = {}
    with open(filename, 'r') as fil:
        counter = 0
        for line in fil:
            event = json.loads(line.strip())
            if 'id' in event:
                user = dict(_id=event['userId'],
                            city=event['city'] if 'city' in event else None,
                            region=event['region'] if 'region' in event else None,
                            country=event['country'] if 'country' in event else None,
                            events=[]
                            )

                my_event = dict(eventId=event['eventId'],
                                articleId=event['id'],
                                deviceType=event['deviceType'],
                                os=event['os'],
                                # url=event['url'],
                                time=event['time'],
                                activeTime=event['activeTime'] if 'activeTime' in event else None,
                                sessionStart=event['sessionStart'],
                                sessionStop=event['sessionStop'],
                                referrerHost=event['referrerHostClass'] if 'referrerHostClass' in event else None,
                                referrerUrl=event['referrerUrl'] if 'referrerUrl' in event else None,
                                referrerNetwork=event[
                                    'referrerSocialNetwork'] if 'referrerSocialNetwork' in event else None,
                                referrerSearchEngine=event[
                                    'referrerSearchEngine'] if 'referrerSearchEngine' in event else None)
                if user['_id'] in output:
                    output[user['_id']]['events'].append(my_event)
                else:
                    user['events'].append(my_event)
                    output[user['_id']] = user
                counter += 1

    return output


def save_clean_one_week_articles(filename: str):
    output = {}
    for i in range(1, 8):
        print("Reading file:", i)
        create_article_dict('../data/2017010' + str(i), output)
    save_dict_as_json('articles', output)


def save_clean_one_week_users(filename: str):
    output = {}
    for i in range(1, 8):
        print("Reading file:", i)
        create_user_dict('../data/2017010' + str(i), output)
    save_dict_as_json('articles', output)


if __name__ == '__main__':
    save_clean_one_week_articles("articles")
    # save_clean_one_week_users("users")
