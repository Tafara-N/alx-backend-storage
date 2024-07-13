#!/usr/bin/env python3

"""
Function that lists all documents in a MongoDB collection.
"""

def list_all(mongo_collection):
    """
    Parameters
        mongo_collection: pymongo collection object

    Return
        List of documents in the collection, otherwise an empty list if no
        document is found.
    """

    return [document for document in mongo_collection.find()]
