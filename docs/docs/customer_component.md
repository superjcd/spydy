# 自定义组件
其实在[自定义解析组件](parsers.md)中已经提及了定义自定义组件的方法， 大致的步骤如下：

 - 根据组件类型，继承一个抽象基类， 以规范组件的行为（子类需要实现特定的方法， 如下所示）spydy现有抽象基类有：

   | 抽象基类名称          | 说明                                                         | spydy默认返回类型     |
   | --------------------- | ------------------------------------------------------------ | --------------------- |
   | spydy.urls.Urls       | 存储及提供url的抽象基类，子类需要实现如下方法：1 `pop`方法， 返回一个字符类型的url  2 `totoal`方法， 子类定义时需要带上@property装饰器， 因为spydy会把`total`当做属性来使用 | `pop`返回字符串       |
   | spydy.request.Request | 网路请求抽象基类， 子类需要实现如下方法： 1 `request` 方法   | [requests.Response](https://requests.readthedocs.io/en/master/api/#requests.Response)对象 |
   | spydy.parsers.Parser  | 解析基类， 子类需要实现如下方法： 1 `parse` 方法             | 字典                  |
   | spydy.filters.Filter  | 过滤基类， 子类需要实现如下方法： 1 `filter` 方法            | 字典                  |
   | spydy.store.Store     | 存储基类， 子类需要实现如下方法： 1 store 方法               | 上一步结果            |
   | spydy.logs.Log        | 打印基类， 子类需要实现如下方法： 1 log 方法                 | 上一步结果            |

   

- 在自定义组件的方法时， 最好输出与spydy的默认返回类型相同类型的结果， 以兼容spydy组件

- 定义`__call__`方法和`__str__`方法， 具体参考[自定义解析组件](parsers.md)


然后在使用的时候， 将自定义组件定义在配置文件的[Pipeline]下即可，记得带上`file:`标签， 请参考[快速开始](quickstart.md)。接着为我们的组件附上自定义参数， 遇到参数较为复杂的情况， 可以参考之前提到的网络请求组件[配置参数](spydy_configs.md)的配置参数的方式。

## 自定义异步组件
因为spydy是通过协程来实现并发的， 如果想要尽可能地提升爬虫速度，可以自定义一个异步组件。不过需要指出的是， 影响爬虫速度最重要的是网络请求， spydy已经实现了相应的异步组件， 即[AsyncHttpRequest](requests.md)； 其次是存储部分（不久也会提供）。因为上诉这些操作是涉及比较多的IO操作的。 这里作为演示， 我们来定义一个自定义异步组件：

```
from spydy.async_component import AsyncComponent
import asyncio

class MyIoOperation(AsyncComponent)
    def __init__(self):
        pass
        
    async def operate(self, inofs):
        await asyncio.sleep(1)
        return infos

    def __call__(self, *args, **kwargs):
        return self.operate(*args, **kwargs)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__repr__()

```

可以看到 ,  我们的 自定义异步组件`MyIoOperation`首先要继承了`AsyncComponent`。然后定义一个`async`方法， 这里是`operate`， 在这里处理涉及到IO的各种操作。总体来说非常简单。    

但需要注意的是， 大多数情况下， 自己定义异步组件是难以提升效果的， 除非你的自定义组件涉及到了大量的IO操作， 类似请求网络以及存储这种过程。





