import abc
import aiohttp
import requests
from requests_html import HTML, AsyncHTMLSession
from .adpaters import url_for_request

__all__ = ["LinearHttpGetRequest", "AsyncHttpGetRequest"]


class Request(abc.ABC):
    @abc.abstractmethod
    def get_html(self):
        ...


class LinearHttpGetRequest(Request):
    def __init__(self, headers=None, proxy=None):  # 把method去掉
        self._headers = headers
        if proxy:
            self._proxy = {"http": proxy, "https": proxy}
        else:
            self._proxy = None

    def get_html(self, url):
        url = url_for_request(url)
        with requests.session() as session:
            return session.get(url, headers=self._headers, proxies=self._proxy)

    def __call__(self, *args, **kwargs):
        return self.get_html(*args, **kwargs)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()


class AsyncHttpGetRequest(Request):
    def __init__(self, headers=None, proxy=None):
        self.Async = ""
        self._headers = headers
        if proxy:
            self._proxy = {"http": proxy, "https": proxy}
        else:
            self._proxy = None

    async def get_html(self, url):
        url = url_for_request(url)
        asession = AsyncHTMLSession()
        response = await asession.get(url, headers=self._headers, proxies=self._proxy)
        return response

    def __call__(self, *args, **kwargs):
        return self.get_html(*args, **kwargs)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()
