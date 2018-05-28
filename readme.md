The project show how to use scrapy with proxy and user-agent crawling websites that free from been forbidden.  
#Skywalk
Skywalk is a collection of scrapy spiders including 58.com,ziroom.com,ke.com,baletu.com and so on. It's a project that means to analysis Housing rental market of china,and aims to supply Business decision for Apartment Operators.
#Require Projects  
Haiproxy, a proxy pool we need to use as a proxy server.
https://github.com/SpiderClub/haipproxy.git
###use agent to scrapy shell
scrapy shell http://sh.58.com/pinpaigongyu/32655300606023x.shtml -s USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"

##mongodb create index
### add uniqe key index
db.house_shanghai.ensureIndex({'uniqe_key':1}, {name: 'uniqe',unique: true,dropDups: true,weights: 100,background: true})  

# 2dsphere index
db.house_shanghai.createIndex( { "position" : "2dsphere" } )  


# full text search index
db.house_shanghai.createIndex( { title: "text", brand: "text" ,city: "text",district: "text",block: "text",address: "text",apartment: "text",traffic: "text",content: "text"} ,{name:'full_text'},{default_language:'hans'})  

#full text search demo
db.house_shanghai.find({$test:{$search:"上海"}})  

# geo search demo  
db.runCommand( {
   geoNear: "house_shanghai",
   near: { type: "Point" , coordinates: [121.671597,31.274732] } ,
   spherical: true,
   maxDistance: 10

} )