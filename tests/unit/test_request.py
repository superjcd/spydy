from spydy.request import HttpRequest
from requests import Response


def test_linearhttpgetrequest():
    url = "https://dmoz-odp.org/"
    lr = HttpRequest()
    assert type(lr(url)) == Response
