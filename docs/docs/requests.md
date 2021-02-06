# 网络请求组件

网络请求组件继承自`spydy.reuqests.Request` 基类， 顾名思义是用来访问网络/请求资源的。spydy的网络请求组件包括 ：

- HttpRequest:  同步网络请求组件
- AsyncHttpRequest： 异步网络请求组件

不论是`HttpReuqest`还是`AsyncHttpRequest` 都只是对[requests](https://requests.readthedocs.io/en/master/)包的`Session`对象的`request`方法进行了一层薄薄的封装， 所以`HttpReuqest`和`AsyncHttpRequest`的参数可以参考[这里](https://requests.readthedocs.io/en/master/api/)， 默认的`method`参数为`GET`。它们的返回值是[requests.Response](https://requests.readthedocs.io/en/master/api/#requests.Response)对象。

