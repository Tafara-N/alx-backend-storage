#!/usr/bin/env python3

"""
Function returns all students sorted by average score with an ordered top DESC
"""


def top_students(mongo_collection):
    """
    Parameters
        mongo_collection: pymongo collection object

    Return
        List of students sorted by average score in descending order
    """

    students_top = mongo_collection.aggregate([
        {"$project": {
            "name": "$name",
            "averageScore": {
                "$avg": "$topics.score"
                }
            }
        },
        {"$sort": {
            "averageScore": -1
            }
        }
    ])

    return students_top
