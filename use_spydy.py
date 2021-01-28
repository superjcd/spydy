from spydy.main import fire
from spydy.urls import RedisListUrls, DummyUrls

# 添加urls
# r = RedisListUrls(list_name="/spider/testurls")

# for _ in range(10):
#     r.push("https://www.dmoz-odp.org/")

# fire()


du = DummyUrls(url="https://dmoz-odp.org/", repeat=10)


for i in range(12):
    print(du())
    
