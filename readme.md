###use agent to scrapy shell
scrapy shell http://sh.58.com/pinpaigongyu/31486368238267x.shtml -s USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"


http://sh.58.com/pinpaigongyu/31486368238267x.shtml


##mongodb create index
### add uniqe key index
db.house_shanghai.ensureIndex({'uniqe_key':1}, {name: 'uniqe',unique: true,dropDups: true,weights: 100,background: true})

### delete index
db.house_shanghai.dropIndex('uniqe_key')