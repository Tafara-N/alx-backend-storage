#!/usr/bin/env python3

"""
Improved '12-log_stats.py' by adding the top 10 of the most present IPs in the
collection nginx of the database logs

12-log_stats.py:
================
Script that provides some stats about Nginx logs stored in MongoDB
    db: logs
    collection: nginx
"""

from pymongo import MongoClient


METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def log_stats(mongo_collection, option=None):
    """
    Script that provides some stats about Nginx logs stored in MongoDB

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

    print("IPs:")

    top_ips = get_top10_ips(nginx_collection)

    for ip in top_ips:
        print(f"\t{ip.get('_id')}: {ip.get('count')}")


def get_top10_ips(mongo_collection):
    """
    Function retrieves the top 10 most common IP addresses

    Parameters
        mongo_collection: pymongo collection object

    Return
        top_ips: pymongo aggregation object
    """

    top_ips = mongo_collection.aggregate([
        {"$group": {
            "_id": "$ip",
            "count": {
                "$sum": 1
                }
            }
        },
        {"$sort": {
            "count": -1
            }
        },
        {"$limit": 10}
    ])

    return top_ips


if __name__ == "__main__":
    nginx_collection = MongoClient(
        "mongodb://127.0.0.1:27017").logs.nginx

    log_stats(nginx_collection)
