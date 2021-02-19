import pytest
from spydy.parsers import XpathParser, CssParser
from spydy.request import HttpRequest


@pytest.fixture(params=["https://dmoz-odp.org/"], name="response")
def get_response(request):
    r = HttpRequest()
    return r(request.param)


def test_xpath_parser(response):
    parser = XpathParser()

    parser._rules = {"editors": "//div[@class='editors']/h3/text()[1]"}

    results = parser(response)

    assert "editors" in results
    assert results["editors"] == "91,929"


def test_css_parser(response):
    parser = CssParser()

    parser._rules = {"editors": "div.editors h3.stat"}

    results = parser(response)

    assert "editors" in results
    assert "91,929" in results["editors"]
