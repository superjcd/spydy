import abc
import csv
import asyncio
from sqlalchemy import create_engine, MetaData, Table
from threading import RLock
from .component import Component, AsyncComponent
from typing import List, Union

# from sqlalchemy.ext.asyncio import create_async_engine

__all__ = ["Store", "CsvStore", "AsyncCsvStore", "DbStore"]


class Store(Component):
    @abc.abstractmethod
    def store(self):
        ...

    def __call__(self, *args, **kwargs):
        return self.store(*args, **kwargs)


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


class AsyncCsvStore(Store, AsyncComponent):
    def __init__(self, file_name):
        self._filename = file_name

    async def store(self, items):
        if items:
            fileds = list(items)
            with open(self._filename, "a+", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fileds)
                async with asyncio.Lock():
                    writer.writerow(items)
            return items


dblock = RLock()


class DbStore(Store):
    def __init__(self, connection_url=None, table_name=None):
        self._connection_url = connection_url
        self._table_name = table_name
        self.engine = create_engine(connection_url, echo=False)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)

    def store(self, items: Union[dict, List[dict]]):
        if items:
            dblock.acquire()
            self.engine.execute(self.metadata.tables[self._table_name].insert(), items)
            dblock.release()
            return items



class AsyncDbStore(Store, AsyncComponent):
    def __init__(self, connection_url=None, table_name=None):
        ...


class AsyncDbManyStore(Store, AsyncComponent):
    def __init__(self, connection_url=None, table_name=None):
        ...
