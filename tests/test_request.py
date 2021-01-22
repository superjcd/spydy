from spydy.request import LinearHttpGetRequest
from requests import Response

def test_linearhttpgetrequest():
    url = "https://dmoz-odp.org/"
    lr = LinearHttpGetRequest()
    assert type(lr(url)) == Response