import abc
import sys
import time
from .exceptions import UrlsStepNotFound
from .utils import print_msg, convert_seconds_to_formal, get_total_from_urls, print_stats_log

__all__ = ["SimplePrintLog", "MessageLog", "StatsReportLog"]


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


class StatsReportLog(Log):
    def __init__(self, every=1):
        self._every = int(every)
        self._urls_instance = None
        self._N = 0
        self._trigger_time = (
            time.time()
        )  # There is a very small bias(cuz this will be called before Urls pop method), but the bias samll enough to ignore
        self._stats = {}

    def init(self):
        if not self._urls_instance:
            raise UrlsStepNotFound
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
            efficiency = 1 if _efficiency>1 else _efficiency
            eta = convert_seconds_to_formal(total_now / consuming_speed)
            self._stats["Elapsed"] = convert_seconds_to_formal(time_elapsed)                    
            self._stats["Processed"] = self._N
            self._stats["Consumed"] = urls_consumed
            self._stats["Remained"] = total_now
            self._stats["Processing Speed"] = processing_speed
            self._stats["Effiency"] = efficiency
            self._stats["Eta"] = eta
            print_stats_log(self._stats)
        return items

    def __call__(self, *args, **kwargs):
        return self.log(*args, **kwargs)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()
