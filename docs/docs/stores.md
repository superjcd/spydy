# 结果存储组件
spydy目前提供了以下存储组件：
 
 - [CsvStore](#csvstore)
 - [DbStore](#dbstore)
 - [DbManyStore](#dbstore)
 - [AsyncDbStore](#asyncdbstore)
 - [AsyncDbManyStore](#asyncdbmanystore)

## CsvStore
将结果输出到`csv`文件， 支持以下参数：
- `file_name`:文件名称， 如果该文件已经存在， 则会以追加写入的方式将结果添加至现有文件的末尾。
  
注意：`CsvStore` 不会写入字段的名称。

## DbStore
将结果输出到关系型数据库 ， 支持以下参数：
- `connection_url`: 数据库连接方式， 采用的是sqlalchemy的连接方式，具体参考[这里](https://docs.sqlalchemy.org/en/13/core/connections.html)
- `table_name`: 结果需要写入的表名， 该表必须要先存在

## DbManyStore
将**多个结果**(List[dict])输出到关系型数据库， 支持以下参数
参数和`DbStore`一致， 用来一次性存储多个结果的， 比如在上一步的输出结果的格式为List[dict]的时候(即[{}, {}])可以使用该组件

# AsyncDbStore
异步存储组件， 开发中(其实是在等sqlalchemy的1.4版本)
## AsyncDbManyStore
异步存储组件（支持同时写入多个数据）， 开发中(其实是在等sqlalchemy的1.4版本)