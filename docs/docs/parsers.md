# 网页（请求）解析组件
请求解析组件通常需要使用者自己提供的（或者也可能是使用者唯一需要定义的组件）， spydy只提供了一个`DmozParser`来获取[dmoz](https://dmoz-odp.org/)网站的部分数据用以测试， 具体参考[快速开始](quickstart.md)。不过spydy还是提供了部分组件来简化繁琐的网页解析工作， 比如：

  - [XpathParser](#xpathparser)
  - [CssParser](#cssparser)
  - [自定义parser](#自定义parser)


## XpathParser

 基于使用者提供的xpath规则， 来解析网络请求对象的结果。只要使用者的自定义类继承了`XpathParser`,  那么只要在自定义类中写入值为xpath规则的类属性， `XpathParser`就会解析相应内容， 以`DmozParser`为例， 它是通过如下方式定义的：

```
class DmozParser(XpathParser):
    editors = "//div[@class='editors']/h3/text()[1]"
    categories = "//div[@class='categories']/h3/text()[1]"
    sites = "//div[@class='sites']/h3/text()[1]"
    languages = "//div[@class='languages']/h3/text()[1]"

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()

```

后续， `XpathParser`就会把类的属性名作为输出结果（字典格式）的键， 类的属性值对应的xpath规则匹配出来的值作为输出结果的值。

## CssParser
同`XpathParser`， 当使用者的自定义类中继承了`CssParser`, 那么只要在自定义类中写入值为csss选择器规则的类属性， `CssParser`就会自动解析目标内容。

## 自定义parser
这里的自定义parser是指不继承上诉的`XpathParser`或者`CssParser`而完全由用户定义的解析组件。
有时候， 网页解析的逻辑会变的很复杂， 比如需要进行一些条件判断，类似当a出现的时候b的值是什么， 或者a的值是b和c的结合。虽然spydy的推荐的做法通常是， 继承spydy的`XpathParser`或者`CssParser`， 然后在[filters](filters.md)这一步去进行更进一步的操作（`spydy.filters.CommonFilter`提供了非常便利的方法）。 比如前面提到的条件判断， 值的清洗之类。  
但有时你可能想直接操作response对象（比如交互解析， 类似[scrapy](https://docs.scrapy.org/en/latest/index.html)的shell功能， 则可以选择在自定义组件中打一个断点），或者你想返回的结果并不是字典，比如是字典的列表， 那么就需要来自己定义一个parser。


下面是一个用来演示的自定义parser：
```
from spydy.parsers import Parser
from requests_html import HTML

class Myparser(Parser): # 继承抽象积累Parser
    def __init__(self):  # any parameters you want to set
        pass

    def parse(self, response):  # must define
        html = HTML(html=response.text)

        content1 = html.xpath('') # define your parse logic here


        return {}  # 通常是字典， 也可以是字典列表， 但是后面的组件需要支持这种返回结果
    
    def __call__(self, *args, **kwargs):
        return self.parse(*args, **kwargs)

    def __str__(self):
        return self.__class__.__name__
```

上面的代码展示了编写自定义parser的一些要点：  

- 首先需要继承spydy的抽象基类`Parser`， 因为`Parser`定义了一个抽象方法`parse`, 所以继承自`Parser` 的自定义解析组件也要定义一个`parse`方法
- `response` 其实就是上一个步骤的返回值， 通常是一个[requests.Response](https://requests.readthedocs.io/en/master/api/#requests.Response)对象（假设`Myparser`的上一步使用的是spydy的自带组件`HttpRequest`或`AsyncRequest`的话）,  所以可以调用response的text属性来获取页面html, 然后进行相应的解析
- 最后返回结果， 一般是一个字典格式。当然也可以是字典列表， 但是后面的组件需要支持这种返回结果。详见[存储组件](stores.md)
- 定义__call__方法， 这个是非常重要的， 因为spydy是默认调用组件的__call__方法的， 所以一定要定义。
- 定义__str__方法， 不是必须的， 但是为了更好地在日志中显示组件， 所以最好加上。

## 返回结果
`Parser组件`最后会返回一个字典(默认)， 或者一个字典列表（某一些自定义场景下）。





