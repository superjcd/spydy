# 过滤组件
过滤组件并不是必须的， 它的作用在很大程度是为了减轻解析组件的工作： 比如清洗解析结果， 生成新结果， 丢弃不要的结果等等。它的存在， 可以让解析组件更加专注于从网页中提取信息， 从而使整个工作流更加的清晰：  
spydy目前提供了一个`CommonFilter`来简化解析的工作， 只需要继承`CommonFilter`， 就能更为清晰地实现丢弃、 保持以及生成新属性的功能。

## CommonFilter
其实在[快速开始](quickstart.md)， 我们就定义了一个自定义过滤组件:

```
from spydy.filters import CommonFilter

class Myfilter(CommonFilter):
    def drops(self):
        return ["editors"]

    def mutates(self, items):
        print("befor_filter: {}".format(items))
        items["sites"] = "0"
        print("after_filter: {}".format(items))
        return items

```
用户的自定义过滤组件可以按需提供三个函数`drops`、 `keeps`和`mutate`, 然后`CommonFilter`就会进行相应地处理：  

- `drops`: 需要返回一个列表， 然后列表中的值所对应的字段将会被丢弃（如果该字段存在于上一步的解析结果中的话）
- `keeps`: 需要返回一个列表， 然后列表中的值所对应的字段将会被保留（如果该字段存在于上一步的解析结果中的话）， 如果一个字段同时出现在`drops`方法的返回结果中时， 以`keeps`方法为准
- `mutates`: `mutate`方法的第一个参数为上一步的解析对象， 这里可以改变解析结果的字段值并输出一个解析结果。 如果解析结果中的字段同时出现在`drops`和`keeps`时， 以`mutates`方法为准。







