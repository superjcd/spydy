from spydy.parsers import XpathParser


class WrongDmozParser(XpathParser):
    editors = "//div[@class='editors']/h3/text()[10]"
    categories = "//div[@class='categories']/h3/text()[10]"
    sites = "//div[@class='sites']/h3/text()[1]"
    languages = "//div[@class='languages']/h3/text()[10]"

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()