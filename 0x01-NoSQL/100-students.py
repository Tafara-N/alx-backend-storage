#!/usr/bin/env python3

"""
Script that provides some stats about Nginx logs stored in MongoDB
    db: logs
    collection: nginx
"""

from pymongo import MongoClient


METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def log_stats(mongo_collection, option=None):
    """
    Parameters
        mongo_collection: pymongo collection object
        option: string - method to search for in collection
    """

    if option:
        value = mongo_collection.count_documents({
            "method": {"$regex": option}
            })

        print(f"\tmethod {option}: {value}")
        return

    results = mongo_collection.count_documents({})
    print(f"{results} logs")
    print("Methods:")

    for method in METHODS:
        log_stats(nginx_collection, method)

    count_results = mongo_collection.count_documents({"path": "/status"})
    print(f"{count_results} status check")


if __name__ == "__main__":
    nginx_collection = MongoClient(
        "mongodb://127.0.0.1:27017").logs.nginx

    log_stats(nginx_collection)
