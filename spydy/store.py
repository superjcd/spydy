import abc
import csv
import asyncio

__all__ = ["CsvStore", "AsyncCsvStore", "StdOutStore"]

class Store(abc.ABC):
    @abc.abstractmethod
    def store():...


class StdOutStore(Store):
    def __init__(self):...

    def store(self, items:dict):
        print(items)

    def __call__(self, *args, **kwargs):
        self.store(*args, **kwargs)

    def __repr__(self):
        return "StdOutStore"

    def __str__(self):
        return self.__repr__()     


class CsvStore(Store):
    def __init__(self, file_name):
        self._filename = file_name

    def store(self, items:dict):
        fileds = list(items)
        with open(self._filename, 'a+', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fileds)
            writer.writerow(items)

    def __call__(self, *args, **kwargs):
        self.store(*args, **kwargs)

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
        with open(self._filename, 'a+', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fileds)
            with await asyncio.Lock():
                writer.writerow(items)

    def __call__(self, *args, **kwargs):
        self.store(*args, **kwargs)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()  

 


if __name__ == "__main__":
    cs = CsvStore(file_name="test.csv")
    cs.store(items={"a":"1", "b":"2"})