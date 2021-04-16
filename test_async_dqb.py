import aiosqlite
import asyncio
from sqlalchemy import text, MetaData, Table
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base

connection_url = "sqlite+aiosqlite:///./tests/files/dmoz.db"


engine = create_async_engine(
        connection_url, echo=False,
    )


async def async_main():  
    async with engine.begin() as conn:
        items1 = {'categories': 3, 'editors': 6, 'languages': 8, 'sites': 10}
        sql = prepare_text_for_multiple_data(items=items1, table_name="stats")
        # print(sql)
        await conn.execute(
             text(sql)
             )


def prepare_text_for_multiple_data(items, table_name):
    if type(items) == dict:
        sql = f"insert into {table_name} ({','.join(list(items.keys()))}) values ({','.join(list(items.values()))})"
        return sql


asyncio.run(async_main())
