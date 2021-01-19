import abc
import aiohttp
import requests
from requests_html import HTML, AsyncHTMLSession

__all__ = ["LinearHttpGetRequest", "AsyncHttpGetRequest"]

class Request(abc.ABC):
    @abc.abstractmethod
    def get_html():...


class LinearHttpGetRequest(Request):
    def __init__(self, headers=None, proxy=None):   # 把mefhod去掉
        self._headers = headers
        if proxy:
            self._proxy = {
                'http': proxy,
                'https': proxy
            }
        else:
            self._proxy = None

    def get_html(self, url):
        with requests.session() as session:
            return HTML(html=session.get(url, headers=self._headers, proxies=self._proxy).text)

    def __call__(self, *args, **kwargs):
        return self.get_html(*args, **kwargs)

    def __repr__(self):
        #return "LinearRequest"
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()
    


class AsyncHttpGetRequest(Request):
    def __init__(self, headers=None, proxy=None):
        self.Async = ""
        self._headers = headers
        if proxy:
            self._proxy = {
                'http': proxy,
                'https': proxy
            }
        else:
            self._proxy = None

    async def get_html(self, url):
        url = url.decode("utf-8")
        asession = AsyncHTMLSession()
        response = await asession.get(url, headers=self._headers, proxies=self._proxy)
        return response.html

    def __call__(self, *args, **kwargs):
        return self.get_html(*args, **kwargs)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()



if __name__ == "__main__":
    from requests_html import HTML

    url = "https://www.dmoz-odp.org/"
    proxies = "http://2120070700089181521:5tGE2ivNSYwlkNs9@forward.apeyun.com:9082"
    lr = LinearHttpGetRequest(proxy=proxies)
    print(lr._proxy)
    response = lr.get_html(url)
    print(response.xpath("//a[@class='logo']/span/text()"))