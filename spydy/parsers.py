import abc
from requests_html import HTML
from .exceptions import TaskWrong


class Cleaner(object):
    @staticmethod
    def clean(text: str):
        return text.strip()


class Parser(abc.ABC):
    @abc.abstractmethod
    def rules(self):
        ...

    @abc.abstractmethod
    def parse(self, response):
        ...


class XpathParser(Parser):
    def __init__(self):
        self._rules = None
        self._result = {}

    def rules(self):
        self._rules = {
            attr: getattr(self, attr)
            for attr in dir(self)
            if not attr.startswith("_") and not callable(getattr(self, attr))
        }
        return self._rules

    def parse(self, response) -> dict:
        if response:
            html = HTML(html=response.text)
            _ = self.rules()
            if self._rules:
                for item, rule in self._rules.items():
                    parsed = html.xpath(rule, first=True)
                    clean_parsed = Cleaner.clean(parsed) if parsed else None
                    self._result[item] = clean_parsed
                return self._result
            return {}

    def __call__(self, *args, **kwargs):
        return self.parse(*args, **kwargs)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()


class CssParser(Parser):
    def __init__(self):
        self._rules = None
        self._result = {}

    def rules(self):
        self._rules = {
            attr: getattr(self, attr)
            for attr in dir(self)
            if not attr.startswith("_") and not callable(getattr(self, attr))
        }
        return self._rules

    def parse(self, response) -> dict:
        if response:
            html = HTML(html=response.text)
            _ = self.rules()
            if self._rules:
                for item, rule in self._rules.items():
                    parsed = html.find(rule, first=True)
                    clean_parsed = Cleaner.clean(parsed) if parsed else None
                    self._result[item] = clean_parsed
                return self._result
            return {}

    def __call__(self, *args, **kwargs):
        return self.parse(*args, **kwargs)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()


# Parser for tests
class DmozParser(XpathParser):
    editors = "//div[@class='editors']/h3/text()[1]"
    categories = "//div[@class='categories']/h3/text()[1]"
    sites = "//div[@class='sites']/h3/text()[1]"
    languages = "//div[@class='languages']/h3/text()[1]"

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()




