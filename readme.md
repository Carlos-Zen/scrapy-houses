The project show how to use scrapy with proxy and user-agent crawling websites that free from been forbidden.  

# Scrapy-houses
Scrapy-houses is a collection of scrapy spiders including 58.com,ziroom.com,ke.com,baletu.com and so on. It's a project that means to analysis Housing rental market of china,and aims to supply Business decision for Apartment Operators.

# How to crawl free from been forbidden.
There are some tips for you.  

## Proxy Tips

### Require Projects  
Haiproxy, a proxy pool we need to use as a proxy server.  
https://github.com/SpiderClub/haipproxy.git
### Setting in scrapy
PROXY_LIST = ['10.6.52.147:3128']

## User-agent Tips

### Always to use agent to scrapy shell
scrapy shell http://sh.58.com/pinpaigongyu/32655300606023x.shtml -s USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"  
### Setting in scrapy
USER_AGENTS = [  
    "Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)",  
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",  
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR   3.0.04506)",  
]  
### Guise as search engine spiders
You can set User-agent the same as google spider or baidu spider.

## Delay Tips

Some websites always recognized spiders by watching the download frequency.So we can set:  
DOWNLOAD_DELAY = (1 or 2 s)  
CONCURRENT_REQUESTS_PER_DOMAIN = 3 ( less than 10 ）  

## Cookie Tips
Disable cookies:  
COOKIES_ENABLED = False  
