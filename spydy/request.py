import abc
import aiohttp
import requests
from requests_html import HTML, AsyncHTMLSession
from .component import Component, AsyncComponent

__all__ = ["HttpRequest", "AsyncHttpRequest"]


class Request(Component):
    @abc.abstractmethod
    def request(self):
        ...

    def __call__(self, *args, **kwargs):
        return self.request(*args, **kwargs)


class HttpRequest(Request):
    def __init__(
        self,
        method="GET",
        headers=None,
        params=None,
        data=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
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
        if proxies:
            self._proxies = {"http": proxies, "https": proxies}
        else:
            self._proxies = None
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
                    headers=self._headers,
                    proxies=self._proxies,
                    params=self._params,
                    data=self._data,
                    cookies=self._cookies,
                    files=self._files,
                    auth=self._auth,
                    timeout=self._timeout,
                    allow_redirects=self._allow_redirects,
                    hooks=self._hooks,
                    stream=self._stream,
                    verify=self._verify,
                    cert=self._cert,
                    json=self._json,
                )


class AsyncHttpRequest(Request, AsyncComponent):
    def __init__(
        self,
        method="GET",
        headers=None,
        params=None,
        data=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
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
        if proxies:
            self._proxies = {"http": proxies, "https": proxies}
        else:
            self._proxies = None
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
        asession = AsyncHTMLSession()
        response = await asession.request(
            self._method,
            url,
            headers=self._headers,
            proxies=self._proxies,
            params=self._params,
            data=self._data,
            cookies=self._cookies,
            files=self._files,
            auth=self._auth,
            timeout=self._timeout,
            allow_redirects=self._allow_redirects,
            hooks=self._hooks,
            stream=self._stream,
            verify=self._verify,
            cert=self._cert,
            json=self._json,
        )
        return response
