# spydy组件
spydy的核心就是一个有序的工作流（Pipeline）, 组成工作流各个步骤的就是各种组件。根据爬虫的各个步骤， spydy自带了多种类型的组件  

- [Url获取组件](urls.md)

- [网络请求组件](requests.md)
- [网页解析组件](parsers.md)
-  [过滤组件](filters.md)
-  [结果存储组件](stores.md)  

**注意**: 每一个spydy组件都继承了一个[抽象基类](https://docs.python.org/zh-cn/3/library/abc.html)用来规范组件的行为（当然使用者在使用的时候是意识不到这些行为的存在的）。例如, 所有的Urls获取组件都继承自`spydy.urls.Urls`基类, 而该基类定义了一个`pop`抽象方法， 用来获取下一个url。

