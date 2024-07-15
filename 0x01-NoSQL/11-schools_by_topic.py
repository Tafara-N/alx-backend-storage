#!/usr/bin/env python3

"""
Function that returns the list of school having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """
    Parameters
        mongo_collection: pymongo collection object
        topic: The topic searched (key)

    Return
        The list of school having a specific topic
    """

    return mongo_collection.find({"topics": topic})
