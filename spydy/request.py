import abc
import aiohttp
import requests
from requests_html import HTML, AsyncHTMLSession
from .component import Component, AsyncComponent
from .utils import run_if_callable

__all__ = ["HttpRequest", "AsyncHttpRequest"]


class Request(Component):
    @abc.abstractmethod
    def request(self):
        ...

    def __call__(self, *args, **kwargs):
        return self.request(*args, **kwargs)


class AsyncRequest(AsyncComponent):
    @abc.abstractmethod
    def request(self):
        ...

    def __call__(self, *args, **kwargs):
        return self.request(*args, **kwargs)


def _prepare_proxies_for_requests(proxies):
    if callable(proxies):
        return proxies
    elif proxies and not callable(proxies):
        return {"http": proxies, "https": proxies}
    else:
        return None


class HttpRequest(Request):
    """
    Normal synchronous http request, and its request method is a thin warpper of requests.Request
    """

    def __init__(
        self,
        method="GET",
        headers=None,
        params=None,
        data=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=10,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
    ):
        self._method = method
        self._headers = headers
        self._proxies = _prepare_proxies_for_requests(proxies)
        self._params = params
        self._data = data
        self._cookies = cookies
        self._files = files
        self._auth = auth
        self._timeout = timeout
        self._allow_redirects = allow_redirects
        self._hooks = hooks
        self._stream = (stream,)
        self._verify = verify
        self._cert = cert
        self._json = json

    def request(self, url):
        if url:
            with requests.session() as session:
                return session.request(
                    self._method,
                    url,
                    headers=run_if_callable(self._headers),
                    proxies=run_if_callable(self._proxies),
                    params=run_if_callable(self._params),
                    data=run_if_callable(self._data),
                    cookies=run_if_callable(self._cookies),
                    files=run_if_callable(self._files),
                    auth=run_if_callable(self._auth),
                    timeout=float(run_if_callable(self._timeout)),
                    allow_redirects=run_if_callable(self._allow_redirects),
                    hooks=run_if_callable(self._hooks),
                    stream=run_if_callable(self._stream),
                    verify=run_if_callable(self._verify),
                    cert=run_if_callable(self._cert),
                    json=run_if_callable(self._json),
                )


class AsyncHttpRequest(AsyncRequest):
    """
    Asynchronous http request, and its request method is a thin wrapper of requests.Request
    """

    def __init__(
        self,
        method="GET",
        headers=None,
        params=None,
        data=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=10,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
    ):
        self._method = method
        self._headers = headers
        self._proxies = _prepare_proxies_for_requests(proxies)
        self._params = params
        self._data = data
        self._cookies = cookies
        self._files = files
        self._auth = auth
        self._timeout = timeout
        self._allow_redirects = allow_redirects
        self._hooks = hooks
        self._stream = (stream,)
        self._verify = verify
        self._cert = cert
        self._json = json

    async def request(self, url):
        if url:
            asession = AsyncHTMLSession()
            response = await asession.request(
                self._method,
                url,
                headers=run_if_callable(self._headers),
                proxies=run_if_callable(self._proxies),
                params=run_if_callable(self._params),
                data=run_if_callable(self._data),
                cookies=run_if_callable(self._cookies),
                files=run_if_callable(self._files),
                auth=run_if_callable(self._auth),
                timeout=float(run_if_callable(self._timeout)),
                allow_redirects=run_if_callable(self._allow_redirects),
                hooks=run_if_callable(self._hooks),
                stream=run_if_callable(self._stream),
                verify=run_if_callable(self._verify),
                cert=run_if_callable(self._cert),
                json=run_if_callable(self._json),
            )
            return response
