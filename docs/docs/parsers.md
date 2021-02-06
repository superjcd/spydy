# 网页（请求）解析组件
请求解析组件通常是需要使用者自己提供的， spydy只提供了一个`DmozParser`来获取[dmoz](https://dmoz-odp.org/)网站的部分数据用以测试， 具体参考[快速开始](quickstart.md)。不过spydy还是提供了部分组件来简化繁琐的网页解析工作， 比如：

- [XpathParser](#xpathparser)

- [CssParser](#cssparser) 
- 自定义parser


## XpathParser

 基于使用者提供的xpath规则， 来解析网络请求对象的结果。只要使用者的自定义类继承了`XpathParser`,  那么只要在自定义类中写入值为xpath规则的类属性， `XpathParser`就会自动解析， 以`DmozParser`为例， 它是通过如下方式定义的：

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

同XpathParser， 只要在使用者的自定义类中继承了`CssParser`, 那么只要在自定义类中写入值为csss选择器规则的类属性， `CssParser`就会自动解析。

## 自定义parser



