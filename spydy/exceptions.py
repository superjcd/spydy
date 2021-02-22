from typing import List

from requests.exceptions import (
    HTTPError,
    ConnectionError,
    ProxyError,
    SSLError,
    Timeout,
    ConnectTimeout,
    ReadTimeout,
    ChunkedEncodingError,
)

_requests_request_exceptions = (
    HTTPError,
    ConnectionError,
    ProxyError,
    SSLError,
    Timeout,
    ConnectTimeout,
    ReadTimeout,
    ChunkedEncodingError,
)


class TaskDone(Exception):
    """
    Indicate that the tasks have be finished gracefully.
    """


class UrlCompleted(TaskDone):
    """
    Taskd done, there are no more urls.
    """

    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return "UrlCompleted: {}".format(self.msg)

    def __str__(self):
        return self.__repr__()


##   Different kinds of erroneous exceptions
class TaskIgnore(Exception):
    """
    Ignore the task
    """


class TaskRunAgain(Exception):
    """
    Run the task again
    """


class TaskWrong(Exception):
    """
    Task Encounter an error
    """


class UnExpectedHandleType(Exception):
    """
    Exception Type not be supported yet
    """


class StepNotFound(Exception):
    """
    Step not found in pipeline
    """


class UrlsNotFound(StepNotFound):
    """
    Step of urls not found in pipeline
    """


class StatsLogNotFound(StepNotFound):
    """
    Step of statslog not found in pipeline
    """


class ExceptionLogNotFound(StepNotFound):
    """
    Step of exceptionlog not found in pipeline
    """


class StepTypeNotSupported(Exception):
    """
    Step type is not stupported
    """


class DummyUrlNotGiven(Exception):
    """
    Url for DummyUrl is not given
    """


## Put together

Exceptions_To_Handle = (TaskWrong,) + _requests_request_exceptions
Exceptions_To_Ignore = (TaskIgnore,)
Exceptions_To_RunAgain = (TaskRunAgain,)
Exceptions_Of_Success = (UrlCompleted,)
