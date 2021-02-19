# Spydy 配置文件
spydy的配置文件是通过使用python自带的[configparser](https://docs.python.org/zh-cn/3.7/library/configparser.html)来进行解析的,  spydy的配置文件大致可以分为以下三块:

- **[Globals](#globals)**： 设置spdydy的全局参数， 比如运行方式和并发量等
- **[PipeLine](#pipeline)**： 定义各个spydy的工作流， 注意这个是按有序来， 靠前的组件将被率先执行
- **[组件参数配置](#组件参数配置)**：  定义spydy组件或者用户自定义组件的参数
作为例子， 可以参考[快速开始](quickstart.md)中的写好的写配置文件

## Globals
定义控制spydy运行的全局变量：

**run_mode**: 这是必须要填写的， 可选项包括：

- `once`:  仅运行一次, 在测试的时候很有用
- `forever`: 单线程， 会一直运行， 直到urls组件中的url耗尽
- `async_once`: 使用异步的方式， 但是只运行一次， 适合异步执行时的测试
- `async_forever`: 使用异步的方式一直运行

**nworkers**: 并发数量， 不过只有当`run_mode`为`async_forever`的时候才有效果。另外由于spydy的并发机制是基于[协程](https://docs.python.org/zh-cn/3/library/asyncio-task.html)的, 所以只有当我们的工作流中包含异步组件(即带有`Async`开头的组件)才会有效果。


**interval**: 爬虫每次运行间的等待时间。  

**recovery_type**: 当程序报错的时候， `urls`[组件](components.md)处理当前url的方式， 目前支持：

 - `skip`: 不做任何事情， 意味着发生错误的url不会被执行第二次， 通常不是理想的选择
 - `url_back_end`: 把出错的url放回队列的最后， 当然前提是`urls`组件是有序的队列， 例如`RedisListUrls`
 - `url_back_front`: 把出错的url放回队列的z最前面， 同样，前提是`urls`组件是有序的队列


## PipeLine
在这里我们需要定义我们的整个工作流， 再强调一次， Pipeline中的组件是按照定义的先后顺序有序执行的。定义的方式通常是“步骤名=组件名”的形式。  
这里的步骤名称可以是任意的， 没有特别的限制， 但是建议使用符合步骤类别的名称， 比如`urls = RedisUrlsList`的方式，虽然可以不使用`urls`作为步骤的名称， 但是很显然， 使用urls作为名称能够使工作流更加清晰易懂。  
在[快速开始的复杂的例子](quickstart.md/#复杂一点的例子)中有一个组件是这样配置的`filter = file:mypkg.filters.Myfilter`, 注意这里的参数值带有一个`file:`标签， 意味着`mypkg.filters.Myfilter`就是[自定义组件](customer_component.md)。所以用户想使用自己的组件的时候（尤其是定义网页解析组件时）， 只要带上`file:`标签spydy就能识别。

## 组件参数配置
组件的参数在这里配置， 由于组件可能会是多个， 所以需要为多个组件配置参数， 配置方式是: 用Pipeline中定义的步骤名作为section名（参考[快速开始](quickstart.md)）， 然后在该section下配置组件的参数， 如果没有为PipeLine中的组件配置参数的话， 那么spydy将会使用组件的默认参数。  
**注意**：
  在配置参数的时候，除了可以使用字符串作为参数值， 同样也可以使用`file:`标签(注意：`file`和`:`是没有空格的)来实现更为复杂的赋值， 比如在配置网络请求组件`HttpRequest`的请求头时， 请求头可能会很大， 所以不适合直接在配置文件中定义。那么我们可以这样配置：
```
[request]
headers = file:myheaders.headers
```
`myheaders`为当前目录下的python(myheaders.py)文件(当然如果把所有的自定义文件放在一个目录下的话， 参数定义就是`mypkg.myheaders.headers`)， `headers`是你准备的请求头， 比如：
```
headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'}
```

`headers`甚至可以是函数（有时候可能需要随机地提供请求头， 这个时候使用函数来提供请求头就有意义了）：
```
def headers():
    return {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'}
```


## 不使用配置文件
通过`spydy`命令在命令行启动spydy并不是spydy的唯一使用方式， 你也可以通过导入spydy的相应模块， 并准备好运行参数(字典格式)来运行spydy:

```
from spydy.engine import Engine
from spydy.utils import check_configs
from spydy import urls, request, parsers, logs, store

myconfig = {
    "Globals":{
        "run_mode": "async_forever",
        "nworkers": "4"
    },
    "PipeLine":[urls.DummyUrls(url="https://dmoz-odp.org", repeat=10),
                request.AsyncHttpRequest(), parsers.DmozParser(), logs.MessageLog(), store.CsvStore(file_name=FILE_NAME)]
    }

chech_configs(myconfig)
spider = Engine.from_dict(myconfig)
spider.run()
```





