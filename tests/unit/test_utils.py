from spydy.utils import convert_seconds_to_standard_format, wrap_exceptions_message
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


def test_wrap_exception():
    msg1 = "less than max_oneline_display"
    wrapped = wrap_exceptions_message(msg1) 
    assert wrapped == repr(msg1) 

    msg2 = msg1 * 2
    wrapped2 = wrap_exceptions_message(msg2)
    print(msg2)
    assert wrapped2 != repr(msg2) 
    assert wrapped2[40:42] == "/n"
