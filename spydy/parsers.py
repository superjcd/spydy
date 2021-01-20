import abc
from requests_html import HTML



class Cleaner(object):
    @staticmethod
    def clean(text:str):  
        return text.strip()


class Parser(abc.ABC):
    @abc.abstractmethod
    def rules(self):...

    @abc.abstractmethod
    def parse(self):...
    

class XpathParser(Parser):
    def __init__(self):
        self._rules = None
        self._result = {}

    def rules(self):
        self._rules = {attr:getattr(self, attr) for attr in dir(self) if not attr.startswith('_') and not callable(getattr(self, attr))}
        return self._rules

    def parse(self, html: HTML) -> dict:
        _ = self.rules()
        if self._rules:
            for item, rule in self._rules.items(): 
                self._result[item] = Cleaner.clean(html.xpath(rule,  first=True))
            return self._result
        return {}

    def __call__(self, *args, **kwargs):
        return self.parse(*args, **kwargs)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()


#Parser for tests
class DmozParser(XpathParser):
    editors = "//div[@class='editors']/h3/text()[1]"
    categories = "//div[@class='categories']/h3/text()[1]"
    sites = "//div[@class='sites']/h3/text()[1]"
    languages = "//div[@class='languages']/h3/text()[1]"

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()
