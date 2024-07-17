#!/usr/bin/env python3

"""
Writing and Reading to/from Redis and recovering original type
"""

import uuid
from typing import Callable, Union

import redis


class Cache():
    """
    Writing strings to Redis
    """

    def __init__(self) -> None:
        """
        Private redis instance and then flush the instance
        """

        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Parameters
            self: Cache instance
            data: Union[str, bytes, int, float] - data to store

        Return
            A string
        """

        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
