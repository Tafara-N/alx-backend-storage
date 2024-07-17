#!/usr/bin/env python3

"""
Writing and Reading to/from Redis and recovering original type
"""

import uuid
from functools import wraps
from typing import Callable, Union

import redis


def call_history(method: Callable) -> Callable:
    """
    Function calls the history decorator

    Parameters
        method: The method to be decorated

    Return
        Callable: The decorated method
    """

    key = method.__qualname__  # type: ignore

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        A wrapper to log inputs and outputs of the given method

        Parameters
            self:
            *args:
            **kwargs:

        Return
            outputs
        """

        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        output = method(self, *args, **kwargs)

        self._redis.rpush(input_key, str(args))
        self._redis.rpush(output_key, str(output))

        return output

    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    Counts how many times methods of the Cache class are called

    Parameters
        method: The method to be decorated

    Return
        Callable: Decorated method
    """

    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to
        """

        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def replay(fn: Callable):
    """
    Displays the history of calls of a particular function

    Parameters
        fn: Callable function
    """

    with redis.Redis() as rds:
        fuction_name = fn.__qualname__  # noqa: F841
        number_of_calls = int(rds.get(function_name) or 0)  # noqa: F821
        print(f"{function_name} was called {number_of_calls} times:")  # noqa: F821

        inputs = [
            i.decode("utf-8") if isinstance(i, bytes) else ""
            for i in rds.lrange(function_name + ":inputs", 0, -1)  # type: ignore
        ]
        outputs = [
            o.decode("utf-8") if isinstance(o, bytes) else ""
            for o in rds.lrange(function_name + ":outputs", 0, -1)  # type: ignore
        ]

        for i, o in zip(inputs, outputs):
            print(f"{function_name}(*{i}) -> {o}")  # type: ignore


class Cache:
    """
    Writing strings to Redis
    """

    def __init__(self) -> None:
        """
        Private redis instance and then flush the instance
        """

        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generates a random key (e.g. using uuid), store the input data in Redis
        using the random key

        Parameters
            self: Cache instance
            data: Union[str, bytes, int, float] - data to store

        Return
            str(uuid.uuid4()): str - key
        """

        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes,
                                                          int, float]:  # type: ignore
        """
        Reading from Redis and recovering original type

        Parameters
            key: Key to get
            fn: Callable function, defaults=None

        Return
            data: Union[str, bytes, int, float]
        """

        key_value = self._redis.get(key)
        return fn(key_value) if fn is not None else key_value

    def get_str(self, key: str) -> str:
        """
        Gets string data type

        Parameters
            key: Key to get

        Return
            str: string
        """

        return self.get(key, lambda x: x.decode("utf-8"))  # type: ignore

    def get_int(self, key: str) -> int:
        """
        Gets integer data type

        Parameters
            key: Key to get

        Return
            int: integer
        """

        return self.get(key, lambda x: int(x))  # type: ignore
