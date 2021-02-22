import abc
import sys
import time
import json
from pprint import pprint
from .component import Component
from .utils import (
    print_msg,
    convert_seconds_to_standard_format,
    get_total_from_urls,
    print_stats_log,
    print_table,
)

__all__ = ["SimplePrintLog", "MessageLog", "StatsReportLog", "ExceptionLog"]


class Log(Component):
    @abc.abstractmethod
    def log(self):
        ...

    def __call__(self, *args, **kwargs):
        return self.log(*args, **kwargs)


class SimplePrintLog(Log):
    def log(self, items):
        pprint(items)
        return items


class MessageLog(Log):
    def __init__(self, info_header="INFO", verbose=False):
        self._info_header = info_header
        self._verbose = verbose

    def log(self, items: dict):
        print_msg(msg=items, info_header=self._info_header, verbose=self._verbose)
        return items


class StatsReportLog(Log):
    def __init__(self, every=1):
        self._every = int(every)
        self._urls_instance = None
        self._N = 0
        self._trigger_time = time.time()
        self._stats = {}

    def init(self, urls_instance):
        self._urls_instance = urls_instance
        self._total = get_total_from_urls(urls_instance=self._urls_instance)

    def log(self, items):
        self._N += 1
        if self._N % self._every == 0 and self._total != None:
            total_now = get_total_from_urls(urls_instance=self._urls_instance)
            urls_consumed = self._total - total_now
            time_elapsed = time.time() - self._trigger_time
            processing_speed = round(self._N / time_elapsed, 2)
            consuming_speed = round(urls_consumed / time_elapsed, 2)
            _efficiency = round(urls_consumed / self._N, 2)
            efficiency = 1 if _efficiency > 1 else _efficiency
            try:
                eta = convert_seconds_to_standard_format(total_now / consuming_speed)
            except ZeroDivisionError:
                eta = "--"
            self._stats["Elapsed"] = convert_seconds_to_standard_format(time_elapsed)
            self._stats["Processed"] = self._N
            self._stats["Consumed"] = urls_consumed
            self._stats["Remained"] = total_now
            self._stats["Processing Speed"] = processing_speed
            self._stats["Efficiency"] = efficiency
            self._stats["Eta"] = eta
            print_stats_log(self._stats)
        return items


class ExceptionLog(Log):
    def __init__(self, every=1):
        self._every = int(every)
        self._exceptions_records = None
        self._N = 0

    def init(self, excepitons):
        self._exceptions_records = excepitons

    def log(self, items):
        self._N += 1
        if self._N % self._every == 0:
            print_table(self._exceptions_records)
        return items
