import redis
conn = redis.Redis()

list_name = "/spider/urls"

for _ in range(30):
    conn.rpush(list_name, 'http://www.baidu.com')