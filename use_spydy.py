from spydy.main import fire
from spydy.urls import RedisListUrls

# 添加urls
r = RedisListUrls(list_name="/spider/testurls")
# for _ in range(1):
#     r.push("https://www.dmoz-odp.org/")

fire()

