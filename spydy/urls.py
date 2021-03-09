import abc
import os
import redis
from .exceptions import UrlCompleted, UnExpectedHandleType, DummyUrlNotGiven
from .component import Component


__all__ = ["DummyUrls", "FileUrls", "RedisListUrls", "RedisSetUrls"]


class Urls(Component):
    @abc.abstractmethod
    def pop(self):
        ...

    @abc.abstractmethod
    def total(self):
        ...

    @abc.abstractmethod
    def handle_exception(self):
        ...

    def __call__(self, *args, **kwargs):
        return self.pop(*args, **kwargs)


class DummyUrls(Urls):
    """
    Genertae one url for given times
    """

    def __init__(self, url=None, repeat: int = 1):
        if not url:
            raise DummyUrlNotGiven
        self._url = url
        self._repeat = int(repeat)
        self._urls = [self._url for _ in range(self._repeat)]
    
    @property
    def total(self):
        return len(self._urls) 

    def pop(self):
        try:
            item = self._urls.pop(0)  # pop first out
        except IndexError:
            import sys

            sys.tracebacklimit = 0
            raise UrlCompleted(
                "No more dummy urls"
                )
        return item

    def add_to_end(self, url):
        self._urls.append(url)
    
    def add_to_front(self, url):
        self._urls.insert(0, url)

    def handle_exception(self, recovery_type, url):
        if recovery_type == "url_back_end":
            self.add_to_end(url)
        elif recovery_type == "url_back_front":
            self.add_to_front(url)
        elif recovery_type == "skip": # do nothing if skip 
            pass
        else:
            raise UnExpectedHandleType
        return None


class FileUrls(Urls):
    def __init__(self, file_name=None):
        self._filename = file_name
        self._urls = self._readurls(file_name)

    @property
    def total(self):
        return len(self._urls)

    def pop(self):
        try:
            item = self._urls.pop(0)  # pop first out
        except IndexError:
            import sys

            sys.tracebacklimit = 0
            raise UrlCompleted(
                "No more item in file: {!r};Task will be shutdown in seconds..".format(
                    self._filename
                )
            )
        return item


    def _readurls(self, file_name):
        if not os.path.exists(file_name):
            raise FileExistsError("No such file: {!r}".format(file_name))
        with open(file_name, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return [line.strip() for line in lines]

    def add_to_end(self, url):
        self._urls.append(url)
    
    def add_to_front(self, url):
        self._urls.insert(0, url)

    def handle_exception(self, recovery_type, url):
        if recovery_type == "url_back_end":
            self.add_to_end(url)
        elif recovery_type == "url_back_front":
            self.add_to_front(url)
        elif recovery_type == "skip": # do nothing if skip 
            pass
        else:
            raise UnExpectedHandleType
        return None


class RedisSetUrls(Urls):
    def __init__(self, set_name, **kwargs):
        self._set_name = set_name
        self._conn = redis.Redis(**kwargs)

    @property
    def total(self):
        """
        Return count of all urls in the set.
        """
        return self._conn.scard(self._set_name)

    def pop(self):
        ''''
         Using redis spop, randomly get a member from set
        '''
        item = self._conn.spop(self._set_name)
        if item:
            return item.decode("utf-8")
        else:
            import sys

            sys.tracebacklimit = 0
            raise UrlCompleted(
                "No value in redis set: {!r};Task will be shutdown in seconds..".format(
                    self._set_name
                )
            )

    def add(self, item):
        self._conn.sadd(self._set_name, item)

    def handle_exception(self, recovery_type, url):
        if recovery_type == "url_back_end":
            self.add(url)
        elif recovery_type == "url_back_front":
            self.add(url)
        elif recovery_type == "skip": 
            pass
        else:
            raise UnExpectedHandleType
        return None

    def close(self):
        self._conn.close()



class RedisListUrls(Urls):
    def __init__(self, list_name, **kwargs):
        self._list_name = list_name
        self._conn = redis.Redis(**kwargs)

    @property
    def total(self):
        """
        Return  count of all urls.
        """
        return self._conn.llen(self._list_name)

    def pop(self):
        item = self._conn.lpop(self._list_name)
        if item:
            return item.decode("utf-8")
        else:
            import sys

            sys.tracebacklimit = 0
            raise UrlCompleted(
                "No value in redis list: {!r};Task will be shutdown in seconds..".format(
                    self._list_name
                )
            )

    def push(self, item):
        self.rpush(item)

    def rpush(self, item):
        self._conn.rpush(self._list_name, item)

    def lpush(slef, item):
        self._conn.lpush(self._list_name, item)

    def handle_exception(self, recovery_type, url):
        if recovery_type == "url_back_end":
            self.rpush(url)
        elif recovery_type == "url_back_front":
            self.lpush(url)
        elif recovery_type == "skip": # do nothing if skip 
            pass
        else:
            raise UnExpectedHandleType
        return None

    def close(self):
        self._conn.close()



