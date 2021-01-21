# Spydy
---
目前虽然有很多的开源的爬虫框架和工具， 但是它们大多无法同时兼顾**用户友好**以及**良好性能**这两个特性。以目前较为流行的爬虫框架scrapy为例， 
虽然支持高并发地爬取网站信息， 但是对于很多新用户来说， 使用门槛还是比较高的， scrapy的整个工作流没有那么直观， 意味着用户需要非常了解scrapy  
的运行机制和生命周期， 同时开发量也并不少。 
所以对于为什么要使用[spydy](https://superjcd.github.io/spydy/)这个问题， 简而言之， spydy可以帮助使用者以最快的速度以及更为直观的方式， 开发和部署高性能的网络爬虫。
## 安装spydy
```
$ pip install spydy
```
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
spydy的工作流在设计上参考了Unix管道， 定义在配置文件[PipeLine]下面的参数其实就是我们spydy会**顺序执行**的各个步骤,  比如在上面的例子中，  
spydy的工作流是这样的：

```
FileUrls -> LinearHttpGetRequest -> DmozParser -> CsvStore
```

每个步骤的产出就是下一步的输入。

当然， 每个步骤可能需要一些参数， 比如FileUrls需要*file_name*参数， 所以需要单独地在[FileUrls]下面配置好*file_name*参数， 如果用户没有提供相应参数，  
那么spydy将使用默认参数。

配置文件中[Globals]下面可以设置spydy的全局参数， 比如这里的run_mode被设置了*once*， 所以在上面例子中， spydy只会将整个工作流执行一次。

### What's Next
---
在真实开发场景中， 我们希望爬虫能够做到：
* 兼容使用者的自定义模块&功能， 比如兼容用户自定的parser模块以及log功能
* 支持并发&异步
* 支持数据持久化， 比如将数据写入数据库

以上这些， 使用spydy都能轻易做到， 详细移步[spydy文档](https://superjcd.github.io/spydy/).
 