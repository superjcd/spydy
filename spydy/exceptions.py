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

