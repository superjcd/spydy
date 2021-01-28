import abc
from .utils import print_msg

__all__ = ["SimplePrintLog", "MessageLog"]


class Log(abc.ABC):
    @abc.abstractmethod
    def log(self):
        ...

class SimplePrintLog(Log):
    def __init__(self):
        ...

    def log(self, items: dict):
        print(items)
        return items

    def __call__(self, *args, **kwargs):
        return self.log(*args, **kwargs)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()


class MessageLog(Log):
    def __init__(self, info_header="INFO", verbose=False):
        self._info_header = info_header
        self._verbose = verbose

    def log(self, items: dict):
        print_msg(msg=items, info_header=self._info_header, verbose=self._verbose)
        return items

    def __call__(self, *args, **kwargs):
        return self.log(*args, **kwargs)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()