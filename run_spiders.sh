#/bin/bash

cd /home/yfeng/skywalk

pkill -9 scrapy
nohup scrapy crawl beike >/tmp/beike.log&
nohup scrapy crawl pinpai58 > /tmp/pinpai.log&
nohup scrapy crawl baletu > /tmp/balatu.log&