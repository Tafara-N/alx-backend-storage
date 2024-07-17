#!/usr/bin/env python3

"""
Function uses the requests module to obtain the HTML content of a particular
URL and returns it
"""

from functools import wraps

import redis
import requests

store = redis.Redis()


def count_url_usage(method):
    """
    Decorator function to count URL usage and cache the data

    Function caches the result of the method for a given URL

    Parameters
        url: URL for which the result should be cached

    Return
        str: Cached HTML content for the given URL
    """

    @wraps(method)
    def wrapper(url):
        """
        Wrapper function to cache the result of the method for a given URL

        Parameters
            url: URL for which the result should be cached

        Return
            str: Cached HTML content for the given URL
        """

        cached_key = f"cached:{url}"
        cached_data = store.get(cached_key)

        if cached_data:
            return cached_data.decode("utf-8")  # type: ignore

        count_key = f"count:{url}"
        html = method(url)

        store.incr(count_key)
        store.set(cached_key, html)
        store.expire(cached_key, 10)
        return html
    return wrapper


@count_url_usage
def get_page(url: str) -> str:
    """
    Simply counts the number of times the function was accessed

    Retrieves the content of the given URL and returns it as a string

    Parameters
        url: The URL to retrieve the content from

    Return
        str: The content of the URL
    """

    response = requests.get(url)
    return response.text
