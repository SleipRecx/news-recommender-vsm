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
                    obj = dict(id=article['id'],
                               title=article['title'],
                               url=article['url'],
                               pluss='pluss' in article['url'],
                               authors=article['author'] if 'author' in article else None,
                               keywords=article['keywords'].split(',') if 'keywords' in article else None,
                               categories=article['category1'].split('|') if 'category1' in article else None,
                               publishTime=article['publishTime'],
                               profiles=article['profile'][3:])
                    output[key] = obj
    return output


def create_user_dict(filename: str) -> Dict:
    output = defaultdict(list)
    with open(filename, 'r') as fil:
        counter = 0
        for line in fil:
            event = json.loads(line.strip())
            if 'id' in event:
                obj = dict(userId=event['userId'],
                           articleId=event['id'],
                           eventId=event['eventId'],
                           url=event['url'],
                           deviceType=event['deviceType'],
                           os=event['os'],
                           city=event['city'] if 'city' in event else None,
                           region=event['region'] if 'region' in event else None,
                           country=event['country'] if 'country' in event else None,
                           time=event['time'],
                           activeTime=event['activeTime'] if 'activeTime' in event else None,
                           sessionStart=event['sessionStart'],
                           sessionStop=event['sessionStop'],
                           referrerHost=event['referrerHostClass'] if 'referrerHostClass' in event else None,
                           referrerUrl=event['referrerUrl'] if 'referrerUrl' in event else None,
                           referrerNetwork=event['referrerSocialNetwork'] if 'referrerSocialNetwork' in event else None,
                           referrerSearchEngine=event['referrerSearchEngine'] if 'referrerSearchEngine' in event else None)
                output[event['userId']].append(obj)
                if counter == 1000:
                    break
                counter += 1
    return output


if __name__ == '__main__':
    users = create_user_dict('data/20170107')
    with open('tjommi.json', 'w') as out_file:
        out_file.write(json.dumps(users, indent=2, ensure_ascii=False))
