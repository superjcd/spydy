import abc
import csv
import asyncio
import redis
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.asyncio import create_async_engine
from threading import RLock
from .component import Component, AsyncComponent
from typing import List, Union
from collections.abc import Iterable
from .utils import prepare_sql_for_dict, prepare_sql_for_list_of_dict

# from sqlalchemy.ext.asyncio import create_async_engine

__all__ = [
    "Store",
    "CsvStore",
    "AsyncCsvStore",
    "DbStore",
    "RedisSetStore",
    "AsyncDbStore",
]


class Store(Component):
    @abc.abstractmethod
    def store(self):
        ...

    def __call__(self, *args, **kwargs):
        return self.store(*args, **kwargs)


class AsyncStore(AsyncComponent):
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


class AsyncCsvStore(AsyncStore):
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
        self._engine = create_engine(connection_url, echo=False)
        self._metadata = MetaData()
        self._metadata.reflect(bind=self._engine)

    def store(self, items: Union[dict, List[dict]]):
        if items:
            dblock.acquire()
            self._engine.execute(
                self._metadata.tables[self._table_name].insert(), items
            )
            dblock.release()
            return items

    def close(self):
        self._engine.close()


class RedisSetStore(Store):
    def __init__(self, set_name, **kwargs):
        self._set_name = set_name
        self._conn = redis.Redis(**kwargs)

    @property
    def total(self):
        return self._conn.scard(self._set_name)

    def store(self, items):
        if items:
            if isinstance(items, Iterable):
                for item in items:
                    self._conn.sadd(self._set_name, item)
            else:
                self._conn.sadd(self._set_name, items)
            return items

    def close(self):
        self._conn.close()


class AsyncDbStore(AsyncStore):
    def __init__(self, connection_url=None, table_name=None):
        self._connection_url = connection_url
        self._table_name = table_name
        self._engine = create_async_engine(connection_url, echo=False)

    async def store(self, items: Union[dict, List[dict]]):
        if items:
            async with engine.begin() as conn:
                if isinstance(items, dict):
                    sql = prepare_sql_for_dict(items, self._table_name)
                if isinstance(items, list):
                    sql = prepare_sql_for_list_of_dict(items, self._table_name)
                await conn.execute(text(sql), [items1, items2, items3])
            return items

    def close(self):
        self._engine.close()