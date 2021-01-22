from spydy.filters import CommonFilter

class Myfilter(CommonFilter):
    def drops(self):
        return ["editors"]

    def mutates(self, items):
        print("befor_filter: {}".format(items))
        items["sites"] = "0"
        print("after_filter: {}".format(items))
        return items
