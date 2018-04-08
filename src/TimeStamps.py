# Project: web-intelligens
# Created: 07.04.18 14:40
# Owner: Espen Meidell

from collections import defaultdict

import pickle
from pymongo import MongoClient
from pprint import pprint
import json

host = "167.99.45.145"
username = "Gsfbretsd"
password = "5erfFSTYUfnd"
db_name = "adressa_ofc"


def mongo_connect(host, username, password, db_name):
    return MongoClient("mongodb://" + username + ':' + password + '@' + host + '/' + db_name)[db_name]


def create_read_times():
    db = mongo_connect(host, username, password, db_name)
    read_times = defaultdict(list)
    print("Connected")
    total = db.user_profiles.count()
    counter = 0
    for user in db.user_profiles.find(batch_size=250):
        for event in user["events"]:
            read_times[event["articleId"]].append(event["time"])
        counter += 1
        if counter % 100 == 0:
            print(counter, "/", total)
    pickle.dump(read_times, open("read_times.p", "wb"))


def create_read_times_test():
    db = mongo_connect(host, username, password, db_name)
    read_times = defaultdict(list)
    print("Connected")
    total = db.test_user_profiles.count()
    counter = 0
    for user in db.test_user_profiles.find(batch_size=250):
        for event in user["events"]:
            read_times[event["articleId"]].append(event["time"])
        counter += 1
        if counter % 100 == 0:
            print(counter, "/", total)
    pickle.dump(read_times, open("read_times_test.p", "wb"))


def find_average_read_time(filename):
    read_times = pickle.load(open(filename, "rb"))
    average_read_times = {}
    for articleId, timestamps in read_times.items():
        average_read_times[articleId] = int(sum(timestamps) / len(timestamps))

    return average_read_times


def find_median_read_time(filename):
    read_times = pickle.load(open(filename, "rb"))
    median_read_times = {}
    for articleId, timestamps in read_times.items():
        timestamps.sort()
        median_read_times[articleId] = timestamps[len(timestamps) // 2]
    return median_read_times


def add_field_to_documents(field_name, value_dict):
    db = mongo_connect(host, username, password, db_name)
    for id in value_dict:
        db.articles.update({"_id": id}, {"$set": {field_name: value_dict[id]}})
    print("Done updating")


def add_field_to_documents_test(field_name, value_dict):
    db = mongo_connect(host, username, password, db_name)
    for id in value_dict:
        db.test_articles.update({"_id": id}, {"$set": {field_name: value_dict[id]}})
    print("Done updating")



if __name__ == '__main__':
    # add_field_to_documents("median_timestamp", find_median_read_time())
    add_field_to_documents_test("median_timestamp", find_median_read_time("read_times_test.p"))
