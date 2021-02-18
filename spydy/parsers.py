import abc
from requests_html import HTML
from .exceptions import TaskWrong
from .component import Component


class Cleaner(object):
    @staticmethod
    def clean(text: str):
        return text.strip()


class Parser(Component):
    @abc.abstractmethod
    def parse(self, response):
        ...

    def __call__(self, *args, **kwargs):
        return self.parse(*args, **kwargs)


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


# Parser for tests
class DmozParser(XpathParser):
    editors = "//div[@class='editors']/h3/text()[1]"
    categories = "//div[@class='categories']/h3/text()[1]"
    sites = "//div[@class='sites']/h3/text()[1]"
    languages = "//div[@class='languages']/h3/text()[1]"

    # def __repr__(self):
    #     return self.__class__.__name__

    # def __str__(self):
    #     return self.__repr__()
