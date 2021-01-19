import abc
import redis
from .exceptions import UrlCompleted

__all__ = ["RedisListUrls"]



class Urls(abc.ABC):
    @abc.abstractmethod
    def pop():...

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
            raise UrlCompleted("No value in redis list: {!r};Task will be shutdown in seconds..".format(self.list_name))
              
    def push(self, item):
        return self._conn.rpush(self.list_name, item)

    def complete(self):  
        print("No value in redis list: {!r}; Task will be shutdown in seconds...".format(self.list_name))


    def __call__(self, *args, **kwargs):
        return self.pop(*args, **kwargs)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()
    
