# Why spydy？

为什么要是用spydy？简单而言Spydy可以帮助使用者以最快的速度以及更为直观的方式， 开发和部署高性能的网络爬虫。  



## 安装spydy

使用pip进行安装：

```
$ pip install spydy
```



## 例子

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
file_name = test.csv
```

最后在命令行启动spydy:

```
$ spydy myconfig.cfg

(someoutputs)
```

接着， 你会发现在当前目录下面出现了test.csv，并且且文件中多了一行我们想要获取的数据。

## 发生了什么？

spydy的工作流在设计上参考了Unix管道， 定义在配置文件[PipeLine]下面的参数其实就是我们spydy会**顺序执行**的各个步骤,  比如在上面的例子中， spydy的工作流是这样的：

```
FileUrls -> LinearHttpGetRequest -> DmozParser -> CsvStore
```

每个步骤的产出就是下一步的输入。

当然， 每个步骤可能需要一些参数， 比如FileUrls需要*file_name*参数， 所以需要单独地在[FileUrls]下面配置好*file_name*参数， 如果用户没有提供相应参数， 那么spydy将使用默认参数。

配置文件中[Globals]下面可以设置spydy的全局参数， 比如这里的run_mode被设置了*once*， 所以在上面例子中， spydy只会将整个工作流执行一次。


## What's Next？

* 深入理解spydy配置文件

* PipeLine及构成

* spydy进阶

  

  

  

  