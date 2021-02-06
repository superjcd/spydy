# Spydy 配置文件

spydy的配置文件是通过使用python自带的[configparser](https://docs.python.org/zh-cn/3.7/library/configparser.html)来进行解析的,  **spydy**的配置文件大致可以分为以下三块：

- **[Globals](#globals)**： 设置spdydy的全局参数， 比如运行方式和并发量等
- **[Pipeline](#pipeline)**： 定义各个spydy的工作流， 注意这个是按有序来， 靠前的组件将被率先执行
- **[组件参数配置](#组件参数配置)**：  定义spydy组件或者用户自定义组件的参数
作为例子， 可以参考[快速开始](quickstart.md)中的写好的写配置文件

## Globals
定义控制spydy运行的全局变量：

**run_mode**: 这是必须要填写的， 可选项包括：

- `once`:  仅运行一次, 在测试的时候很有用
- `forever`: 单线程， 会一直运行， 直到urls组件中的url耗尽
- `async_once`: 使用异步的方式， 但是只运行一次， 适合异步执行时的测试
- `async_forever`: 使用异步的方式一直运行

**nworkers**: 同时运行的协程数量， 不过只有当`run_mode`为`async_forever`的时候才有效果。



**interval**: 爬虫每次运行间的等待时间。  

**recovery_type**: 当程序报错的时候， `urls`[组件](components.md)处理当前url的方式， 目前支持：

 - `skip`: 不做任何事情， 意味着发生错误的url不会被执行第二次， 通常不是理想的选择
 - `url_back_last`: 把出错的url放回队列的最后， 当然前提是`urls`组件是有序的队列， 例如`RedisListUrls`
 - `url_back_first`: 把出错的url放回队列的z最前面， 同样，前提是`urls`组件是有序的队列


## Pipeline
在这里我们需要定义我们的整个工作流， 再强调一次， Pipeline中的组件是按照定义的先后顺序有序执行的。定义的方式通常是将spydy组件名称（或者是自定义组件， 区分大小写）赋给一个自定义的步骤名称， 这里的步骤名称可以是任意的， 没有特别的限制， 但是建议使用符合步骤类别的名称， 比如`urls=RedisUrlsList`的方式，虽然可以不使用`urls`作为步骤名称， 但是显然， 使用urls作为名称能够使工作流更加清晰易懂。  
在[快速开始的复杂的例子](quickstart.md/#复杂一点的例子)中有一个组件是这样配置的`filter = file:mypkg.filters.Myfilter`, 注意这里的参数值带有一个`file:`标签， 意味着`mypkg.filters.Myfilter`就是自定义组件。所以用户想使用自己的组件的时候（尤其是定义网页解析组件时）， 只要带上`file:`标签spydy就能识别。

## 组件参数配置
组件的参数在这里配置， 由于组件可能会是多个， 所以需要为多个组件配置参数， 配置方式是: 用组件名作为section名（参考[快速开始](quickstart.md)）， 如果没有为PipeLine中的组件配置参数的话， 那么spydy将会使用组件的默认参数。

## 不使用配置文件
通过`spydy`命令在命令行启动spydy并不是spydy的唯一使用方式， 你也可以通过导入spydy的相应模块， 并准备好运行参数(字典格式)来运行spydy:

```
from spydy.engine import Engine
from spydy.utils import check_configs

configs = {
    "Globals": {"run_mode": "async_forever", "nworkers": "4", "recovery_type":"url_back_last"},
    "PipeLine": {
        "url": "DummyUrls",
        "request": "AsyncHttpRequest",
        "parser": "DmozParser",
        "log" : "MessageLog",         
        "store": "CsvStore",
    },
    "DummyUrls": {"url": "https://dmoz-odp.org/, "repeat":"10"},
    "CsvStore": {"file_name": "B07YWBG2XH.csv"},
}

check_configs(configs)
engine = spydy.engine.Engine(configs)
engine.run()
```





