from spydy.request import HttpGetRequest
from requests import Response

def test_linearhttpgetrequest():
    url = "https://dmoz-odp.org/"
    lr = HttpGetRequest()
    assert type(lr(url)) == Response