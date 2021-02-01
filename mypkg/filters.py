from spydy.filters import CommonFilter

class Myfilter(CommonFilter):
    def drops(self):
        return ["editors"]

    def mutates(self, items):
        items["sites"] = "0"
        return items
