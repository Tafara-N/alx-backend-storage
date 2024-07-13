#!/usr/bin/env python3

"""
Function that inserts a new document in a collection based on `kwargs`
"""


def insert_school(mongo_collection, **kwargs):
    """
    Parameters
        mongo_collection: pymongo collection object
        kwargs: dictionary with data to insert

    Return
        _id of the new document
    """

    return mongo_collection.insert_one(kwargs).inserted_id
