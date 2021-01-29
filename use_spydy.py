from spydy.main import fire
from spydy.urls import RedisListUrls, DummyUrls

# 添加urls
r = RedisListUrls(list_name="/spider/testurls")

for _ in range(10):
    r.push("https://www.dmoz-odp.org/")

# print(r.total)
fire()



# import sys
# import time
# for i in range(100):
#     print("noise")
#     sys.stdout.write("Download progress: %d%%   \r" % (i))
#     time.sleep(0.2)
#     sys.stdout.flush()


