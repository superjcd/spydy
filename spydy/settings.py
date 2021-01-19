# Redis connection
RHOST = 'localhost'
RPORT = 6479
QUEUE_NAME = 'urls'

# 目标 https://www.dmoz-odp.org/ 

# 设置代理
Proxy = 'http://2120070700089181521:5tGE2ivNSYwlkNs9@forward.apeyun.com:9082'


# 请求头
Headers =  {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh,zh-CN;q=0.9',
            'cache-control': 'no-cache',
            # 'cookie': self.cookie,
            'cookie': 'session-id=130-3096614-6620765; session-id-time=2082787201l; i18n-prefs=USD; ubid-main=134-5362632-5702960; skin=noskin; session-token=xVNoMO2529I5s8JwXKtzjLRe7Zb7+cfRvcDYGrp5mHBheXNYvY5bMM8Afw2xxGcCvm/qXMUwMYYnvTrxXqiwTuTSlvT8YoCozE3sAgGIsau2t3lN/8rmwMC1ldE1laAkWLeDDfC2C4cB/nB+IsdSjSK/sRsnWXdcQ4GCx9xaNBrIAgwoMPVrsUnoplUa1B4hxQuNIZcw9pb31ayGW2uMxfROApNTFj2DWgXO+kI47WYmZ9VzY6CJb8bKOqqWIIrI; lc-main=en_US; csm-hit=tb:s-229YB59PEG7V1DAFBH1A|1605577844325&t:1605577845660&adb:adblk_no',
            'downlink': '1.35',
            'ect': '3g',
            'pragma': 'no-cache',
            'rtt': '300',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        }

# 设置并发数量
Workers = 4 

