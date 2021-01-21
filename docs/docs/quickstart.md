## 一个简单的例子
---
作为演示， 我们将爬取网站[dmoz](https://dmoz-odp.org/)首页下方的一些统计数据， 如图所示：

![dmoz](../img/dmoz.png)

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
request = LinearHttpGetRequest
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
FileUrls ⇨ LinearHttpGetRequest ⇨ DmozParser ⇨ CsvStore
```

接着， 你会发现在当前目录下面出现了dmoz.csv，并且在dmoz.csv文件中多了一行我们想要获取的数据。

### 发生了什么？
---
spydy的工作流在设计上参考了Unix管道， 定义在配置文件[PipeLine]下面的参数其实就是我们spydy会**顺序执行**的各个步骤,  比如在上面的例子中， spydy的工作流是这样的：

```
FileUrls -> LinearHttpGetRequest -> DmozParser -> CsvStore
```

每个步骤的产出就是下一步的输入。

当然， 每个步骤可能需要一些参数， 比如FileUrls需要*file_name*参数， 所以需要单独地在[FileUrls]下面配置好*file_name*参数， 如果用户没有提供相应参数， 那么spydy将使用默认参数。

配置文件中[Globals]下面可以设置spydy的全局参数， 比如这里的run_mode被设置了*once*， 所以在上面例子中， spydy只会将整个工作流执行一次。

## 一个复杂点的例子
---
在真实开发中， 我们希望爬虫能够做到：
* 兼容使用者的自定义模块&功能， 比如兼容用户自定的parser模块以及log功能
* 支持并发&异步
* 支持数据持久化， 比如将数据写入数据库

OK， 以上这些spydy都可以做到。进入正题之前， 请确保：  

* 有一个可以访问的redis键值存储数据库，当然我们需要在Redis中写入一些URL：  
 
```
from spydy.urls import RedisListUrls

r = RedisListUrls(list_name="/spider/testurls")
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
当然， 你的redis连接和数据库连接(使用sqlalchemy的定义方式)和上面的未必相同， 请根据自己的情况进行修改。

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
---
### spydy无缝兼容用户自定义模块
---
在PipeLine中我们加入了自定义的过滤模块（继承自spydy.filters.CommonFilter），由于filter被定义在parser的后面， 所以filter会处理parsers的结果。在这个过程中如上面日志中显示的那样， 结果数据发生了改变（字段editor没了， sites变成了0）。

### spydy支持并发
---
在*myconfig2.cfg*配置文件的[Globals]全局变量中， 我们将run_mode设置成了*async*， 同时将*num_workers*设置成了4， 意味着spydy将并发执行四个异步任务， 这也就是为什么上面的这个任务会被快速执行完成。

### spydy提供便利的组件
---
利用spdydy自带的持久化组件， 只要在配置文件中简单的配置参数就能够实现对数据的存储。



  

  

  