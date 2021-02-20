from spydy.utils import convert_seconds_to_standard_format
import pytest


def test_convert_seconds_to_formal():
    seconds = 3601
    assert convert_seconds_to_standard_format(seconds) == "1h:0m:1s"

    seconds = 3661
    assert convert_seconds_to_standard_format(seconds) == "1h:1m:1s"

    seconds = 61
    assert convert_seconds_to_standard_format(seconds) == "0h:1m:1s"

    seconds = 1
    assert convert_seconds_to_standard_format(seconds) == "0h:0m:1s"
