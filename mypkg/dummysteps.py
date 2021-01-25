

class DummyClassRaiseError():
    def raise_error(self):
        ve = ValueError("This a Dummy class")
        ve.url = "www.1.org"
        raise ve

    def __call__(self):
        return self.raise_error()

    def __repr__(self):  
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()


class DummyClassCatchError():
    def catch_error(self, items):
        try:
            res = items
        except ValueError as e:
            print(e.args)
            raise   

    def __call__(self):
        return self.catch_error()


    def __repr__(self):  
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()


