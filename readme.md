###use agent to scrapy shell
scrapy shell http://sh.58.com/pinpaigongyu/32655300606023x.shtml -s USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"


http://sh.58.com/pinpaigongyu/31486368238267x.shtml

https://sh.zu.ke.com/zufang/

### collections name
"house_beijing",
"house_chengdu",
"house_chongqing",
"house_guangzhou",
"house_hangzhou",
"house_nanjing",
"house_shanghai",
"house_suzhou",
"house_tianjin",
"house_wuhan",
"house_xian",
"house_zhengzhou",

##mongodb create index
### add uniqe key index
db.house_shanghai.ensureIndex({'uniqe_key':1}, {name: 'uniqe',unique: true,dropDups: true,weights: 100,background: true})
db.house_beijing.ensureIndex({'uniqe_key':1}, {name: 'uniqe',unique: true,dropDups: true,weights: 100,background: true})
db.house_chengdu.ensureIndex({'uniqe_key':1}, {name: 'uniqe',unique: true,dropDups: true,weights: 100,background: true})
db.house_chongqing.ensureIndex({'uniqe_key':1}, {name: 'uniqe',unique: true,dropDups: true,weights: 100,background: true})
db.house_guangzhou.ensureIndex({'uniqe_key':1}, {name: 'uniqe',unique: true,dropDups: true,weights: 100,background: true})
db.house_hangzhou.ensureIndex({'uniqe_key':1}, {name: 'uniqe',unique: true,dropDups: true,weights: 100,background: true})
db.house_nanjing.ensureIndex({'uniqe_key':1}, {name: 'uniqe',unique: true,dropDups: true,weights: 100,background: true})
db.house_suzhou.ensureIndex({'uniqe_key':1}, {name: 'uniqe',unique: true,dropDups: true,weights: 100,background: true})
db.house_tianjin.ensureIndex({'uniqe_key':1}, {name: 'uniqe',unique: true,dropDups: true,weights: 100,background: true})
db.house_wuhan.ensureIndex({'uniqe_key':1}, {name: 'uniqe',unique: true,dropDups: true,weights: 100,background: true})
db.house_xian.ensureIndex({'uniqe_key':1}, {name: 'uniqe',unique: true,dropDups: true,weights: 100,background: true})
db.house_zhengzhou.ensureIndex({'uniqe_key':1}, {name: 'uniqe',unique: true,dropDups: true,weights: 100,background: true})

### delete index
db.house_shanghai.dropIndex('uniqe_key')


# 2dsphere index
db.house_shanghai.createIndex( { "position" : "2dsphere" } )
db.house_beijing.createIndex ({"position" : "2dsphere" })
db.house_chengdu.createIndex ({"position" : "2dsphere" })
db.house_chongqing.createIndex ({"position" : "2dsphere" })
db.house_guangzhou.createIndex ({"position" : "2dsphere" })
db.house_hangzhou.createIndex ({"position" : "2dsphere" })
db.house_nanjing.createIndex ({"position" : "2dsphere" })
db.house_shanghai.createIndex ({"position" : "2dsphere" })
db.house_suzhou.createIndex ({"position" : "2dsphere" })
db.house_tianjin.createIndex ({"position" : "2dsphere" })
db.house_wuhan.createIndex ({"position" : "2dsphere" })
db.house_xian.createIndex ({"position" : "2dsphere" })
db.house_zhengzhou.createIndex ({"position" : "2dsphere" })


db.runCommand( {
   geoNear: "house_shanghai",
   near: { type: "Point" , coordinates: [121.671597,31.274732] } ,
   spherical: true,
   maxDistance: 10

} )

SON([('geoNear','house_shanghai'),('near',SON([('type','Point'),('coordinates',[121.671597,31.274732] )])),('maxDistance',10),('spherical',True)])