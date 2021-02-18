# Spydy中的错误处理机制

你不能指望爬虫永远不会出错， 所以良好的错误处理机制对于爬虫而言是必须的。在配置文件中的[全局参数](spydy_configs.md#Globals)设置中有提到过`recovery_type`参数的设置， spydy默认的`recovery_type`是`url_back_end`， 意味着爬取出错的url会被默认放到队列的最后， 然后等待被再次执行。

除了定义全局性的恢复机制（recovery_type），有些情景下我们希望针对个每个目标url实行不同的处理机制， 比如：

 

- 重跑任务
- 忽略该url
- 挂起程序

只要使用者raise一个相应的错误， spydy就会进行相应的错误处理， 具体见如下：



## 触发全局错误处理机制的异常

spydy的网络请求机制是基于requests包的封装，当spydy运行过程中遇到如下错误（也就是定义在requests中的各种请求错误）的时候后，就会自动触发全局错误处理机制， 也就是采用`recovery_type`定义的方法来处理报错的url。这些错误包括：

-  HTTPError

- *ConnectionError*

-  ProxyError

- SSLError

- Timeout

- ConnectTimeout

- ReadTimeout

上诉错误的含义， 具体参见requests的[异常说明](https://requests.readthedocs.io/en/master/_modules/requests/exceptions/)。除了这些错误以外， 用户还可以通过raise一个`spydy.exceptions.TaskWrong`来触发全局处理机制。



## 触发重跑任务的异常

 当用户在自定义组件中raise了一个`spydy.exceptions.TaskRunAgain`异常时， 那么该url就会被放置到队列末尾（队列有序的情况， 如`RedisListUrls`的情况下， 不然的话可能只是放回， 不一定是尾部）， 等待被再次处理。

## 触发忽略任务的异常

 当用户在自定义组件中raise了一个`spydy.exceptions.TaskIgnore`异常时， 那么该url就会被忽略， 不再执行任何操作。所以用户需要谨慎处理， 在合适的场景下抛出该错误。

## 触发挂起程序的异常

除了上诉提及的异常以外， 其他的所有异常， 都会使spydy挂起。



---

当spydy程序完成以后， 如果没有任何异常的话（也就是没有触发上面提到的任何一种异常）， spydy会在终端打印如下信息：

```
😊 Completed! Spydy ran successfully without any excepitons
```

如果遇到任何异常的话（程序没有被挂起的情况下）， spydy就会按照错误的类型以及出现的次数将异常打印出来，可以作为后续改良爬虫的参考。