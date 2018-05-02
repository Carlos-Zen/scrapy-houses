#/bin/bash

cd /home/yfeng/skywalk

pkill -9 scrapy
/home/yfeng/local/bin/scrapy crawl beike > /tmp/beike.log
/home/yfeng/local/bin/scrapy crawl pinpai58 > /tmp/pinpai.log
/home/yfeng/local/bin/scrapy crawl baletu > /tmp/baletu.log
/home/yfeng/local/bin/scrapy crawl ziroom > /tmp/ziroom.log
/home/yfeng/local/bin/scrapy crawl danke > /tmp/danke.log