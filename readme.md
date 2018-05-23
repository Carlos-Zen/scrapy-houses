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

# full text search index
db.house_shanghai.createIndex( { title: "text", brand: "text" ,city: "text",district: "text",block: "text",address: "text",apartment: "text",traffic: "text",content: "text"} ,{name:'full_text'},{default_language:'hans'})
db.house_beijing.createIndex( { title: "text", brand: "text" ,city: "text",district: "text",block: "text",address: "text",apartment: "text",traffic: "text",content: "text"} ,{name:'full_text'},{default_language:'hans'})
db.house_chengdu.createIndex( { title: "text", brand: "text" ,city: "text",district: "text",block: "text",address: "text",apartment: "text",traffic: "text",content: "text"} ,{name:'full_text'},{default_language:'hans'})
db.house_chongqing.createIndex( { title: "text", brand: "text" ,city: "text",district: "text",block: "text",address: "text",apartment: "text",traffic: "text",content: "text"} ,{name:'full_text'},{default_language:'hans'})
db.house_guangzhou.createIndex( { title: "text", brand: "text" ,city: "text",district: "text",block: "text",address: "text",apartment: "text",traffic: "text",content: "text"} ,{name:'full_text'},{default_language:'hans'})
db.house_hangzhou.createIndex( { title: "text", brand: "text" ,city: "text",district: "text",block: "text",address: "text",apartment: "text",traffic: "text",content: "text"} ,{name:'full_text'},{default_language:'hans'})
db.house_nanjing.createIndex( { title: "text", brand: "text" ,city: "text",district: "text",block: "text",address: "text",apartment: "text",traffic: "text",content: "text"} ,{name:'full_text'},{default_language:'hans'})
db.house_suzhou.createIndex( { title: "text", brand: "text" ,city: "text",district: "text",block: "text",address: "text",apartment: "text",traffic: "text",content: "text"} ,{name:'full_text'},{default_language:'hans'})
db.house_tianjin.createIndex( { title: "text", brand: "text" ,city: "text",district: "text",block: "text",address: "text",apartment: "text",traffic: "text",content: "text"} ,{name:'full_text'},{default_language:'hans'})
db.house_wuhan.createIndex( { title: "text", brand: "text" ,city: "text",district: "text",block: "text",address: "text",apartment: "text",traffic: "text",content: "text"} ,{name:'full_text'},{default_language:'hans'})
db.house_xian.createIndex( { title: "text", brand: "text" ,city: "text",district: "text",block: "text",address: "text",apartment: "text",traffic: "text",content: "text"} ,{name:'full_text'},{default_language:'hans'})
db.house_zhengzhou.createIndex( { title: "text", brand: "text" ,city: "text",district: "text",block: "text",address: "text",apartment: "text",traffic: "text",content: "text"} ,{name:'full_text'},{default_language:'hans'})

#full text search demo
db.house_shanghai.find({$test:{$search:"上海"}})

# geo search demo
db.runCommand( {
   geoNear: "house_shanghai",
   near: { type: "Point" , coordinates: [121.671597,31.274732] } ,
   spherical: true,
   maxDistance: 10

} )

SON([('geoNear','house_shanghai'),('near',SON([('type','Point'),('coordinates',[121.671597,31.274732] )])),('maxDistance',10),('spherical',True)])


# 数量统计
db.house_shanghai.count()
db.house_beijing.count()
db.house_chengdu.count()
db.house_chongqing.count()
db.house_guangzhou.count()
db.house_hangzhou.count()
db.house_nanjing.count()
db.house_suzhou.count()
db.house_tianjin.count()
db.house_wuhan.count()
db.house_xian.count()
db.house_zhengzhou.count()


# 高德账号
13881835007

ff1234