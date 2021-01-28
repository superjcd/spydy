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


class StatisticLog(Log):
    """

    目标：
      统计运行次数， 这个每次log的时候打印即可， 规定每隔几步进行打印

      爬虫成功率： url totoal / 运行次数。 后者容易得到， 前者话需要引用url对象，调用url对象的totoal函数（property）

      显示的结果又：1 运行次数  2 url剩余数， url消耗数 3 成功率， eta：预计完成时间。4 立项情况要对根据error进行统计
    """

    def __init__(self, every=1):
        ...
