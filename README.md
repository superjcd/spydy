![logo](./docs/docs/img/spydy.svg)  

---

目前虽然有很多的开源的爬虫框架和工具， 但是它们大多无法同时兼顾**用户友好**以及**良好性能**这两个特性。
所以对于为什么要使用[spydy](https://superjcd.github.io/spydy/)这个问题， 简而言之， spydy可以帮助使用者以最快的速度以及更为直观的方式， 开发和部署高性能的网络爬虫。
## 安装spydy
```
$ pip install spydy
```
## 一个简单的例子
作为演示， 我们将爬取网站[dmoz](https://dmoz-odp.org/)首页(可能需要梯子)下方的一些统计数据， 如图所示：

![dmoz](./docs/docs/img/dmoz.png) 


首先准备好需要爬取的链接，我们把目标连接放入到urls.txt中:

```
https://dmoz-odp.org
```

然后准备好一个简单的配置文件（myconfig.cfg）：

```
[Globals]
run_mode = once   

[PipeLine]
url = FileUrls
request = HttpGetRequest
parser = DmozParser
store = CsvStore

[FileUrls]
file_name = urls.txt

[CsvStore]
file_name = dmoz.csv
```

最后在命令行启动spydy:

```
$ spydy myconfig.cfg

Your pipeline looks like :
FileUrls ⇨ HttpGetRequest ⇨ DmozParser ⇨ CsvStore
```

接着， 你会发现在当前目录下面出现了dmoz.csv，并且在dmoz.csv文件中多了一行我们想要获取的数据。

### 发生了什么？

spydy的工作流在设计上参考了Unix管道， 定义在配置文件[PipeLine]下面的参数其实就是我们spydy会**顺序执行**的各个步骤,比如在上面的例子中, spydy的工作流是这样的：

```
FileUrls -> HttpGetRequest -> DmozParser -> CsvStore
```

每个步骤的产出就是下一步的输入。

当然， 每个步骤可能需要一些参数， 比如FileUrls需要`file_name`参数， 所以需要单独地在[FileUrls]下面配置好`file_name`参数， 如果用户没有提供相应参数，  
那么spydy将使用默认参数。

配置文件中[Globals]下面可以设置spydy的全局参数， 比如这里的`run_mode`被设置了`once`， 所以在上面例子中spydy只会将整个工作流执行一次。

## 一个复杂点的例子
在真实开发开发场景中， 我们希望爬虫能够做到:  
-兼容使用者的自定义模块&功能， 比如兼容用户自定义网页解析模块
-支持并发&异步
-支持数据持久化， 比如将数据写入数据库...

OK， 以上这些spydy都可以支持。我们再来看一个稍微复杂一点的例子作为演示， 在此之前请确保：  

* 有一个可以访问的redis键值存储数据库，当然我们需要在Redis中写入一些URL：  
 
```
from spydy.urls import RedisListUrls

r = RedisListUrls(list_name="/spider/testurls")  # 默认localhost
for _ in range(10):
    r.push("https://www.dmoz-odp.org/")  
```
 

* 一个可以访问的关系型数据， 在数据库建立一个名为dmoz的database， 以及一个名为stats的表， 表中需要包含editors, categories, sites, languages这四个字段（都是字符串类型）。
  
* 准备好一个文件夹(mypkg), 用于存储用户的自定义模块。mypkg的目录长这样：
```
- mypkg
  - __init__.py
  - filters.py
```
在filters.py中写入：
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

最后， 准备好我们的spydy配置文件(myconfig2.cfg)：
```
[Globals]
run_mode = async
nworkers = 4

[PipeLine]
url = RedisListUrls
request = AsyncHttpGetRequest
parser = DmozParser
filter = file:mypkg.filters.Myfilter
store = DbStore

[RedisListUrls]
host = localhost
port = 6379
list_name = /spider/testurls

[DbStore]
connection_url = sqlite:///./tests/files/dmoz.db
table_name = stats
```
当然， 你的redis连接和数据库连接(使用[sqlalchemy](https://docs.sqlalchemy.org/en/13/core/connections.html)的定义方式)和上面的未必相同， 请根据自己的情况进行修改。

万事俱备， 让我们运行spydy吧：
```
$ spydy myconfig2.cfg

Your pipeline looks like :
RedisListUrls ⇨ AsyncHttpGetRequest ⇨ DmozParser ⇨ Myfilter ⇨ DbStore

befor_mutate: {'categories': '1,031,722', 'languages': '90', 'sites': '3,861,202'}
after_mutate: {'categories': '1,031,722', 'languages': '90', 'sites': '0'}
befor_mutate: {'categories': '1,031,722', 'languages': '90', 'sites': '3,861,202'}
after_mutate: {'categories': '1,031,722', 'languages': '90', 'sites': '0'}
befor_mutate: {'categories': '1,031,722', 'languages': '90', 'sites': '3,861,202'}
after_mutate: {'categories': '1,031,722', 'languages': '90', 'sites': '0'}
befor_mutate: {'categories': '1,031,722', 'languages': '90', 'sites': '3,861,202'}
after_mutate: {'categories': '1,031,722', 'languages': '90', 'sites': '0'}
...

```
### 发生了什么？
### spydy可以无缝兼容用户的自定义模块
我们在*PipeLine*中我们加入了自定义的过滤模块(继承自`spydy.filters.CommonFilter`)，由于**filter**被定义在**parser**的后面， 所以**filter**会处理从**parsers**返回的结果。在这个过程中, 如上面日志中显示的那样， 结果数据发生了改变(sites变成了0).

### spydy可以支持并发
spydy通过**协程**支持并发。在*myconfig2.cfg*配置文件的*[Globals]*部分下， 我们将run_mode设置成了`async`， 同时将`num_workers`设置成了4，同时我们把**request**过程从`HttpGetRequest`改为`AsyncHttpGetRequest`, 意味着spydy将并发执行四个异步任务。这样网络请求就会以异步的方式进行。

```
Tips:
   通常可以通过spydy组件的名称来确定一个组件是不是支持异步的， 如果组件带有Async前缀， 那么该组件就是支持异步的。
```

### spydy提供便利的组件
在上面的例子中， 我们使用了spydy的*RedisListUrls*来获取url, 同时利用spdydy自带的持久化组件，来快速地存储数据。spydy通过为使用者提供常见的组件， 来大大简化使用者的开发工作。

## What's Next
想要了解spydy的更多特性， 请移步[spydy文档](https://superjcd.github.io/spydy/).
 