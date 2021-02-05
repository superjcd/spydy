# Spydy 配置文件

**spydy**的配置文件是通过使用python自带的[configparser](https://docs.python.org/zh-cn/3.7/library/configparser.html)来进行解析的,  **spydy**的配置文件大致可以分为以下三块：

- **[Globals](#globals)**： 设置spdydy的全局参数， 比如运行方式和并发量等。
- **[Pipeline](#pipeline)**： 定义各个spydy的工作流， 注意这个是按有序来， 靠前的组件将被率先执行。
- **[组件参数配置](#组件参数配置)**：  定义spydy组件或者用户自定义组件的参数。
作为例子， 可以参考[快速开始](quickstart.md)中的衣蛾写配置文件。

## Globals

## Pipeline

## 组件参数配置

## 不使用配置文件
通过`spydy`命令在命令行启动spydy并不是spydy的唯一使用方式， 你也可以通过导入spydy的相应模块， 并准备好运行参数(字典格式)来运行spydy:

```
from spydy.engine import Engine
from spydy.utils import check_configs

configs = {
    "Globals": {"run_mode": "async_forever", "nworkers": "4", "recovery_type":"url_back_last"},
    "PipeLine": {
        "url": "DummyUrls",
        "request": "AsyncHttpGetRequest",
        "log" : "MessageLog", 
        "parser": "DmozParser",
        "store": "CsvStore",
    },
    "DummyUrls": {"url": "https://dmoz-odp.org/, "repeat":"10"},
    "CsvStore": {"file_name": "B07YWBG2XH.csv"},
}

check_configs(configs)
engine = spydy.engine.Engine(configs)
engine.run()
```





