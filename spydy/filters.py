import abc
from requests_html import HTML

class Filter(abc.ABC):
    @abc.abstractmethod
    def filter(parsed:dict):...
    

class CommonFilter(Filter):
    def __init__(self):
        self._parsed = None
        self._outputs = None

    def filter(self, parsed):
        self._parsed = parsed  
        self._outputs = parsed

        if hasattr(self, 'drops'):
            drop_items =  getattr(self, 'drops')() 
            if drop_items:
                if isinstance(drop_items, list):
                    for item in drop_items:
                        del self._outputs[item]
                else:
                    raise TypeError("Method Drops of {!r} returned a none-list object".format(self.__class__.__name__))

        if hasattr(self, 'keeps'):
            keep_items = getattr(self, 'keeps')()
            if keep_items:
                self._outputs = {} 
                if isinstance(keep_items, list):
                    for item in keep_items:
                        self._outputs[item] = self._parsed[item]
                else:
                    raise TypeError("Method Keeps of {!r} returned a none-list object".format(self.__class__.__name__))

        if hasattr(self, 'mutates'):
            mutate_items = getattr(self, 'mutates')(self._parsed)
            if mutate_items:
                if isinstance(mutate_items, dict):
                    self._outputs.update(mutate_items)
                else:
                    raise TypeError("Method mutates  of {!r} returned a none-dict object".format(self.__class__.__name__))
        return self._outputs

    def __call__(self, *args, **kwargs):
        return self.filter(*args, **kwargs)

    def __repr__(self):  # 这里需要改一下， 和xpather， 尽量使用子类自己的名字
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()

        
        
class MyFilter(CommonFilter):
    def __init__(self):
        ...

    def drops(self):  
        ...

    def keeps(self):
        ...
    
    def mutates(self, items):
        res = items['item1'] + items['item2']
        return [1]

    


if __name__ == "__main__":
    mf = MyFilter()
    result = mf.filter({"item1":"1", "item2": "2"})
    print(result)








        