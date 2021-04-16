import abc


class Component(abc.ABC):
    @abc.abstractmethod
    def __call__(self):
        ...

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()


class AsyncComponent(Component):
    Async = True
