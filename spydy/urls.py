import abc
import os
import redis
from .exceptions import UrlCompleted, UnExpectedHandleType

__all__ = ["FileUrls", "RedisListUrls"]


class Urls(abc.ABC):
    @abc.abstractmethod
    def pop(self):
        ...


class FileUrls(Urls):
    def __init__(self, file_name=None):
        self._filename = file_name
        self._lines = self._readlines(file_name)

    def pop(self):
        try:
            item = self._lines.pop(0)
        except IndexError:
            import sys

            sys.tracebacklimit = 0
            raise UrlCompleted(
                "No more item in file: {!r};Task will be shutdown in seconds..".format(
                    self._filename
                )
            )
        return item

    def _readlines(self, file_name):
        if not os.path.exists(file_name):
            raise FileExistsError("No such file: {!r}".format(file_name))
        with open(file_name, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return [line.strip() for line in lines]

    def __call__(self, *args, **kwargs):
        return self.pop(*args, **kwargs)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()


class RedisListUrls(Urls):
    def __init__(self, list_name, host="localhost", port=6379):
        self.list_name = list_name
        self._conn = redis.Redis(host=host, port=port)

    def pop(self):
        item = self._conn.lpop(self.list_name)
        if item:
            return item
        else:
            import sys

            sys.tracebacklimit = 0
            raise UrlCompleted(
                "No value in redis list: {!r};Task will be shutdown in seconds..".format(
                    self.list_name
                )
            )

    def rpush(self, item):
        return self._conn.rpush(self.list_name, item)

    def lpush(slef, item):
        return self._conn.lpush(self.list_name, item)

    def handle_exception(self, handle_type, url):
        if handle_type == "url_back_last":
            self.rpush(url)
        elif handle_type == "url_back_first":
            self.lpush(url)
        else:
            raise UnExpectedHandleType
        return None

    def complete(self):
        print(
            "No value in redis list: {!r}; Task will be shutdown in seconds...".format(
                self.list_name
            )
        )

    def __call__(self, *args, **kwargs):
        return self.pop(*args, **kwargs)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()
