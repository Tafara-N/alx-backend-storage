#!/usr/bin/env python3

"""
Function that changes all topics of a school document based on the name
"""


def update_topics(mongo_collection, name, topics):
    """
    Parameters
        mongo_collection: pymongo collection object
        name: The school to update (key)
        topics: The list of topics approached in the school (value)
    """

    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
