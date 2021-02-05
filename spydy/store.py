import abc
import csv
import asyncio
from sqlalchemy import create_engine, MetaData, Table
from threading import RLock

# from sqlalchemy.ext.asyncio import create_async_engine

__all__ = ["CsvStore", "AsyncCsvStore", "DbStore"]


class Store(abc.ABC):
    @abc.abstractmethod
    def store(self):
        ...


class CsvStore(Store):
    def __init__(self, file_name):
        self._filename = file_name

    def store(self, items: dict):
        if items:
            fileds = list(items)
            with open(self._filename, "a+", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fileds)
                writer.writerow(items)
            return items

    def __call__(self, *args, **kwargs):
        return self.store(*args, **kwargs)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()


class AsyncCsvStore(Store):
    def __init__(self, file_name):
        self.Async = ""
        self._filename = file_name

    async def store(self, items):
        items = await items
        fileds = list(items)
        with open(self._filename, "a+", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fileds)
            with await asyncio.Lock():
                writer.writerow(items)
        return items

    def __call__(self, *args, **kwargs):
        return self.store(*args, **kwargs)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()


dblock = RLock()

class DbStore(Store):
    def __init__(self, connection_url=None, table_name=None):
        self._connection_url = connection_url
        self._table_name = table_name
        self.engine = create_engine(connection_url, echo=False)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)

    def store(self, items: dict):
        dblock.acquire()
        self.engine.execute(self.metadata.tables[self._table_name].insert(), items)
        dblock.release()
        return items

    def __call__(self, *args, **kwargs):
        return self.store(*args, **kwargs)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()


class AsyncDbStore(Store):
    def __init__(self, connection_url=None, table_name=None):
        self.Async = ""

