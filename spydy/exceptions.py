from typing import List

from requests.exceptions import (
    HTTPError,
    ConnectionError,
    ProxyError,
    SSLError,
    Timeout,
    ConnectTimeout,
    ReadTimeout,
)

_requests_request_exceptions = (
    HTTPError,
    ConnectionError,
    ProxyError,
    SSLError,
    Timeout,
    ConnectTimeout,
    ReadTimeout,
)


"""
    Successful Exceptions
"""


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


"""
  Different kinds of erroneous exceptions
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
    '''
     Step not found in pipeline
    '''

class UrlsStepNotFound(StepNotFound):
    """
    Step of urls not found in pipeline
    """


class StepTypeNotSupported(Exception):
    """
    Step type is not stupported
    """


class DummyUrlNotGiven(Exception):
    """
    Url for DummyUrl is not given
    """


Exceptions_To_Handle = (TaskWrong, ) + _requests_request_exceptions
Exceptions_Of_Success = (UrlCompleted,)
