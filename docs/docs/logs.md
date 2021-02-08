# 打印日志
spydy没有选择使用[logging](https://docs.python.org/zh-cn/3/howto/logging.html)等功能强大的日志模块来实现日志功能， 相反地spydy提供了一些非常简单的组件来打印日志：

  - [SimplePrintLog](#simpleprintlog) 
  - [MessageLog](#MessgeLog) 
  - [StatsReportLog](#statsreportlog)


## SimplePrintLog
简单地打印信息， 没有任何参数。通常可以用来调试，查看爬虫的中间结果， 比如可以定义在[存储组件](stores.md)之前。 
## MessageLog
打印缩略的信息以及执行时间信息。有时后，中间解析结果可能会很大， 所以可以选择只打印缩略结果。支持以下参数：

 - `info_header`: 打印信息的信息头， 默认为"INFO"
 - `verbose`: 是否支持详细打印， 如果为True, 那么会打印所有信息；Flase的话则打印缩略信息


## StatsReportLog
滚动打印统spydy目前的运行结果， 参数如下：
 - `every` : 每运行多少次打印当前统计结果， 默认值为1。
打印示例如下:
```
  Elapsed: 0h:0m:35s| Processed: 124| Consumed: 125| Remained: 9| Processing Speed: 3.47| Efficiency: 1| Eta: 0h:0m:2s|
```
统计字段的意思如下：

| 字段名           | 说明                                                         |
| ---------------- | ------------------------------------------------------------ |
| Elapsed          | 爬虫运行时间                                                 |
| Processed        | 运行次数                                                     |
| Consumed         | 成功处理的url个数（正常是<=Processed, 但在并发条件下可能或略微大于上面） |
| Remained         | 剩余url个数                                                  |
| Processing Speed | 每秒运行次数， Processed/Elapsed                             |
| Efficiency       | 爬虫运行效率， Consumed/Processed，<=1(在爬虫运行失败的时候， 根据[recovery_type](spydy_configs.md)的类型， url可能会被放回Urls组件， 所以消耗的url数量可能会小于运行次数 |
| Eta              | 预计剩余时间                                                 |




如果使用者想要结合[logging](https://docs.python.org/zh-cn/3/howto/logging.html)来实现功能更为丰富的日志打印功能， 完全可通过定义一个[自定义组件](customer_component.md)来实现。

