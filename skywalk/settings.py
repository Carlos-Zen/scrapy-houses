# -*- coding: utf-8 -*-

# Scrapy settings for skywalk project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'skywalk'

SPIDER_MODULES = ['skywalk.spiders']
NEWSPIDER_MODULE = 'skywalk.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'skywalk (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.25
DOWNLOAD_TIMEOUT = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'skywalk.middlewares.SkywalkSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'scrapy_splash.SplashCookiesMiddleware': 723,
    # 'scrapy_splash.SplashMiddleware': 725,
    'skywalk.middlewares.RandomUserAgent': 1,
    'skywalk.middlewares.ProxyMiddleware': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
    'scrapy.extensions.closespider.CloseSpider': 100,
}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'skywalk.pipelines.MongoPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

USER_AGENTS = [
    "Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)",
    # "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    # "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    # "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    # "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    # "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    # "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    # "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    # "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    # "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    # "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    # "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    # "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    # "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    # "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    # "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)"
]

SPLASH_URL = 'http://10.18.98.134:8050'

# mongodb
MONGO_URI = 'mongodb://10.6.52.147:27017'
MONGO_DATABASE = 'house'
MONGO_COLLECTION_PRE = 'house_%s'
MONGO_DATABASE_COLLISION = 'house_collision'
MONGO_COLLECTION_COLLISION = 'collision'

# PROXIES
PROXY_LIST = ['10.6.52.147:3128']

# crawl control
CRAWL_PAGE = 100
# CLOSESPIDER_ERRORCOUNT = 300
# duplate control
DUPS_LIMIT = 3000
DUPS_STOP = False  # 去重中断任务
DUPS_KEYS = ['city', 'district', 'rent_type', 'address', 'orientation', 'room_area', 'floor', 'building_floor',
             'rental', 'lati', 'longi', 'apartment', 'bedroom_type', 'room_num', 'hall_num', 'bathroom_num']
HOUSE_KEYS = ['city', 'district', 'rent_type', 'address', 'orientation', 'room_area', 'floor', 'building_floor',
              'lati', 'longi', 'apartment', 'bedroom_type', 'room_num', 'hall_num', 'bathroom_num']
# city and start urls
CITYS = {
    'shanghai': '上海',
    'beijing': '北京',
    'chengdu': '成都',
    'chongqing': '重庆',
    'hangzhou': '杭州',
    'wuhan': '武汉',
    'xian': '西安',
    'zhengzhou': '郑州',
    'suzhou': '苏州',
    'shenzhen': '深圳',
    'guangzhou': '广州',
    'tianjin': '天津',
    'nanjing': '南京',
}
START_URLS = {
    'baletu': [
        'http://sh.baletu.com/zhaofang/',
        'http://bj.baletu.com/zhaofang/',
        'http://cd.baletu.com/zhaofang/',
        'http://cq.baletu.com/zhaofang/',
        'http://wh.baletu.com/zhaofang/',
        'http://xa.baletu.com/zhaofang/',
        'http://zz.baletu.com/zhaofang/',
        'http://hz.baletu.com/zhaofang/',
        'http://suzhou.baletu.com/zhaofang/',
        'http://gz.baletu.com/zhaofang/',
        'http://nj.baletu.com/zhaofang/',
        'http://tj.baletu.com/zhaofang/',
    ],
    'pinpai58': [
        'http://sh.58.com/pinpaigongyu/',
        'http://bj.58.com/pinpaigongyu/',
        'http://cd.58.com/pinpaigongyu/',
        'http://cq.58.com/pinpaigongyu/',
        'http://wh.58.com/pinpaigongyu/',
        'http://xa.58.com/pinpaigongyu/',
        'http://zz.58.com/pinpaigongyu/',
        'http://hz.58.com/pinpaigongyu/',
        'http://gz.58.com/pinpaigongyu/',
        'http://nj.58.com/pinpaigongyu/',
        'http://tj.58.com/pinpaigongyu/',
    ],
    'beike': [
        'http://sh.zu.ke.com/zufang/',
        'http://bj.zu.ke.com/zufang/',
        'http://cd.zu.ke.com/zufang/',
        'http://cq.zu.ke.com/zufang/',
        'http://wh.zu.ke.com/zufang/',
        'http://xa.zu.ke.com/zufang/',
        'http://zz.zu.ke.com/zufang/',
        'http://hz.zu.ke.com/zufang/',
        'http://gz.zu.ke.com/zufang/',
        'http://nj.zu.ke.com/zufang/',
        'http://tj.zu.ke.com/zufang/',
    ],
    'ziroom': [
        'http://sh.ziroom.com/z/nl/z3.html',
        'http://www.ziroom.com/z/nl/z3.html',
        'http://cd.ziroom.com/z/nl/z3.html',
        'http://cq.ziroom.com/z/nl/z3.html',
        'http://wh.ziroom.com/z/nl/z3.html',
        'http://xa.ziroom.com/z/nl/z3.html',
        'http://zz.ziroom.com/z/nl/z3.html',
        'http://hz.ziroom.com/z/nl/z3.html',
        'http://gz.ziroom.com/z/nl/z3.html',
        'http://nj.ziroom.com/z/nl/z3.html',
        'http://tj.ziroom.com/z/nl/z3.html',
    ],
    'danke': [
        'https://www.dankegongyu.com/room/sh',
        'https://www.dankegongyu.com/room/bj',
        'https://www.dankegongyu.com/room/cd',
        'https://www.dankegongyu.com/room/cq',
        'https://www.dankegongyu.com/room/wh',
        'https://www.dankegongyu.com/room/xa',
        'https://www.dankegongyu.com/room/zz',
        'https://www.dankegongyu.com/room/hz',
        'https://www.dankegongyu.com/room/gz',
        'https://www.dankegongyu.com/room/nj',
        'https://www.dankegongyu.com/room/tj',
    ]

}
