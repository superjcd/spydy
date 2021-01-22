import abc


__all__ = ["StdOutLog"]


class Log(abc.ABC):
    @abc.abstractmethod
    def log(self):
        ...


class StdOutLog(Log):
    def __init__(self):
        ...

    def log(self, items: dict):
        print(items)
        return items

    def __call__(self, *args, **kwargs):
        return self.log(*args, **kwargs)

    def __repr__(self):
        return "StdOutStore"

    def __str__(self):
        return self.__repr__()
