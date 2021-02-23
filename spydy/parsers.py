import abc
import re
from requests_html import HTML, Element
from .mixins import RuleBasedParserMixin
from .exceptions import TaskWrong
from .component import Component

__all__ = ["XpathParser", "CssParser", "DmozParser"]


class Cleaner(object):
    @staticmethod
    def clean(tobe_cleaned):
        if isinstance(tobe_cleaned, str):
            return Cleaner.clean_text(tobe_cleaned)

        if isinstance(tobe_cleaned, Element):
            return Cleaner.clean_element(tobe_cleaned)

    @staticmethod
    def clean_text(text: str):
        return text.strip()

    @staticmethod
    def clean_element(element: Element):
        if hasattr(element, "text"):
            return Cleaner.clean_text(element.text)


class Parser(Component):
    @abc.abstractmethod
    def parse(self, response):
        ...

    def __call__(self, *args, **kwargs):
        return self.parse(*args, **kwargs)


class XpathParser(Parser, RuleBasedParserMixin):
    """
    Parse contents by xpath rules, often act as a parent class to be inheritate.
    """

    def __init__(self):
        self._rules = None
        self._result = {}

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


class CssParser(Parser, RuleBasedParserMixin):
    """
    Parse contents by css selectors, often act as a parent class to be inheritate.
    """

    def __init__(self):
        self._rules = None
        self._result = {}

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


#
class LinksParser(Parser):
    """
    Extract the links in the reponse html content
    """

    def __init__(self, pattern=None, use_re=False):
        self._pattern = pattern
        self._use_re = bool(use_re)

    def parse(self, response):
        html = HTML(html=response.text)
        links = response.html.links
        return links


class RegexParser(Parser):
    def __init__(self):
        ...

    def parse(self, response):
        ...
