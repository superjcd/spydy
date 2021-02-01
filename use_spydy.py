from spydy.main import fire
from spydy.urls import RedisListUrls, DummyUrls
from spydy.utils import print_stats_log

# 添加urls
r = RedisListUrls(list_name="/spider/testurls")

for _ in range(100):
    r.push("https://www.dmoz-odp.org/")

# print(r.total)
fire()




