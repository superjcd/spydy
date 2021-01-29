import abc
import sys
import time
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


class StatsReportLog(Log):
    def __init__(self, every=1):
        self._every = every
        self._urls_instance = None  
        self._N = 0  
        self._position_in_pipeline = None
        self._total = get_total_from_urls(urls_instance=self._urls_instance, position) # 获取一次
        self._trigger_time = time.time()  # 或有细微误差
        self._stats = {}

    def log(self, items):
        self._N += 1 
        if self._N % self._every == 0 and self._total != None:
            total_now = get_total_from_urls(urls_instance=self._urls_instance, position) #根据position 决定要不要+1
            urls_consumed = self._total - total_now
            time_elapsed = time.time() - self._trigger_time()
            processing_speed = round(self._N /time_elapsed, 2)
            consuming_speed = round(urls_consumed /time_elapsed, 2)
            efficency = round(urls_consumed/self._N, 2)
            eta = convert_seconds_to_formal(self._total / consuming_speed)  # convert to %h%m%s
            self._stats["Elapsed"] = round(time_elapsed, 2)
            self._stats["Processed"] = self._N
            self._stats["Consumed"] = urls_consumed
            self._stats["Remained"] = total_now
            self._stats["Processing Speed"] = processing_speed
            self._stats["Effiency"] = efficency
            print_stats_log()  
            
        return items
    
