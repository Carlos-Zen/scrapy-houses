#/bin/bash

cd /home/yfeng/skywalk

pkill -9 scrapy
nohup /home/yfeng/local/bin/scrapy crawl beike >/tmp/beike.log&
nohup /home/yfeng/local/bin/scrapy crawl pinpai58 > /tmp/pinpai.log&
nohup /home/yfeng/local/bin/scrapy crawl baletu > /tmp/baletu.log&
nohup /home/yfeng/local/bin/scrapy crawl ziroom > /tmp/ziroom.log&
nohup /home/yfeng/local/bin/scrapy crawl danke > /tmp/danke.log&