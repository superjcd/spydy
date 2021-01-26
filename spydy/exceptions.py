from typing import List


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


class TaskWrong(Exception):
    """
    Task Encounter an error
    """


class UnExpectedHandleType(Exception):
    """
    Exception Type not be supported yet
    """


class StepNotFoundError(Exception):
    """
    Step not found in pipeline
    """


class StepTypeNotSupported(Exception):
    """
    Step type is not stupported
    """
