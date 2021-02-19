import abc
import copy
from requests_html import HTML
from .component import Component

__all__ = ["CommonFilter"]


class Filter(Component):
    @abc.abstractmethod
    def filter(self, to_filter: dict):
        ...

    def __call__(self, *args, **kwargs):
        return self.filter(*args, **kwargs)


class CommonFilter(Filter):
    def __init__(self):
        self._to_filter = None
        self._outputs = None

    def filter(self, to_filter):
        if to_filter:
            self._to_filter = copy.deepcopy(to_filter)
            self._outputs = copy.deepcopy(to_filter)

            if hasattr(self, "drops"):
                drop_items = getattr(self, "drops")()
                if drop_items:
                    if isinstance(drop_items, list):
                        for item in drop_items:
                            if item in self._outputs:
                                del self._outputs[item]
                    else:
                        raise TypeError(
                            "Method Drops of {!r} returned a none-list object".format(
                                self.__class__.__name__
                            )
                        )

            if hasattr(self, "keeps"):
                keep_items = getattr(self, "keeps")()
                if keep_items:
                    self._outputs = {}
                    if isinstance(keep_items, list):
                        for item in keep_items:
                            if item in self._to_filter:
                                self._outputs[item] = self._to_filter[item]
                    else:
                        raise TypeError(
                            "Method Keeps of {!r} returned a none-list object".format(
                                self.__class__.__name__
                            )
                        )

            if hasattr(self, "mutates"):
                mutate_items = getattr(self, "mutates")(self._outputs)
                if mutate_items:
                    if isinstance(mutate_items, dict):
                        self._outputs.update(mutate_items)
                    else:
                        raise TypeError(
                            "Method mutates of {!r} returned a none-dict object".format(
                                self.__class__.__name__
                            )
                        )
            return self._outputs
