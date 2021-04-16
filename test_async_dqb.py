import aiosqlite
import asyncio
from collections import Iterable
from sqlalchemy import text, MetaData, Table
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base

connection_url = "sqlite+aiosqlite:///./tests/files/dmoz.db"


engine = create_async_engine(
        connection_url, echo=False,
    )

items1 = {'categories': 3, 'editors': "uuuu", 'languages': 8, 'sites': 10}
items = {}
async def async_main():  
    async with engine.begin() as conn:
        
        sql = prepare_sql_for_execute(items, "stats")
        # sql = prepare_text_for_multiple_data(items=items1, table_name="stats")
        # print(sql)
        await conn.execute(
             text(sql), [items1]
             )

# 假设数据位空， 我应该应该返回一个标志， 然后不去执行！
def prepare_sql_for_execute(items, table_name):
    if isinstance(items, dict):
        item_keys = items.keys()
        col_names = ','.join(item_keys)
        placeholders = ','.join([':' + col for col in item_keys])
        sql = f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})"
        return sql


asyncio.run(async_main())
# print(prepare_text_for_multiple_data(items1, "stats"))