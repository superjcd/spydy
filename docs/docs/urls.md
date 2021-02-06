# Url获取组件
Url获取组件顾名思义， 使用来存储urls以及获取url的组件；spydy提供了以下Url获取组件：

- [DummyUrls](#dummyurls)

- [FileUrls](#fileurls)
- [RedisSetUrls](#redisseturls)
- [RedisListUrls](#redislisturls)


## DummyUrls
用来重复地产生某一个url， 通常是用来测试的（比如有些网站在重复访问多次的时候， 会有访问限制， 所以通过对一个网站的多次访问可以触发网站的反爬机制）。参数有：
- `url`: url连接, 必选项
- `repeat`: 重复次数, 默认为1


## FileUrls
作用和`DummyUrls`类似， 通常用来测试， 不过可以在在文件中存储更多不同的url, 参数有:
- `file_name`: 文件名称, 记录在file中的url需要以换号符分隔

## RedisSetUrls
连接redis的set,  所以存储在`RedisSetUrls`的urls是不能重复且无序的， 参数有:
- `set_name`: redis集合名称
- `host`: 连接host
- `port`: 连接port

## RedisListUrls
连接redis的list,  所以存储在`RedisListUrls`的urls是可以重复且有序的，参数有:
- `list_name`: redis队列名称
- `host`: 连接host
- `port`: 连接port