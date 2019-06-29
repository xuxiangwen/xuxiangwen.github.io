## ik中文分词 +  同义词Synonym 

###  添加同义词文件

~~~shell
rm -rf ./config/analysis-ik/synonym.txt
touch ./config/analysis-ik/synonym.txt
echo 西红柿, 番茄 >> ./config/analysis-ik/synonym.txt
cat ./config/analysis-ik/synonym.txt
~~~

### 创建index

~~~shell
curl -X DELETE "localhost:9200/test_ik_synonym?pretty"
curl -XPUT 'localhost:9200/test_ik_synonym?pretty' -H 'Content-Type: application/json' -d'
{
  "settings": {
    "analysis": {
      "analyzer": {
        "ik_max_word_synonym": { 
          "type": "custom",
          "tokenizer": "ik_max_word",
          "filter": ["ik_synonym_filter"]
        }
      },
      "filter": {
        "ik_synonym_filter": {
          "type": "synonym",
          "synonyms_path": "analysis-ik/synonym.txt"
        }
      }  
    }
  },
  "mappings": {
      "properties": {
        "content": {
          "type": "text",
          "analyzer": "ik_max_word_synonym",
          "search_analyzer": "ik_max_word_synonym"
        }
      }
  }
}
'

curl -X GET 'localhost:9200/test_ik_synonym?pretty'
~~~

### 插入document

~~~shell
curl -H 'Content-Type: application/json'  -XPOST http://localhost:9200/test_ik_synonym/_doc/1?pretty -d'
{"content":"我的女儿非常喜欢吃西红柿炒鸡蛋和清炒土豆丝"}
'

curl -H 'Content-Type: application/json'  -XPOST http://localhost:9200/test_ik_synonym/_doc/2?pretty -d'
{"content":"我的女儿非常喜欢吃番茄炒鸡蛋和清炒马铃薯丝"}
'

curl -XGET 'localhost:9200/test_ik_synonym/_search?size=10&pretty=true'
~~~

### 查询

番茄, 西红柿之前可以相互匹配, 以下两个查询都可以匹配到两个文档. 

~~~shell
curl -H 'Content-Type: application/json'  -XPOST http://localhost:9200/test_ik_synonym/_search?pretty  -d'
{
    "query" : { "match" : { "content" : "西红柿" }},
    "highlight" : {
        "pre_tags" : ["<tag1>", "<tag2>"],
        "post_tags" : ["</tag1>", "</tag2>"],
        "fields" : {
            "content" : {}
        }
    }
}
'

curl -H 'Content-Type: application/json'  -XPOST http://localhost:9200/test_ik_synonym/_search?pretty  -d'
{
    "query" : { "match" : { "content" : "番茄" }},
    "highlight" : {
        "pre_tags" : ["<tag1>", "<tag2>"],
        "post_tags" : ["</tag1>", "</tag2>"],
        "fields" : {
            "content" : {}
        }
    }
}
'
~~~

但是, 土豆和马铃薯之前还是不能互相匹配. 以下两个查询只可以匹配到一个文档.

~~~shell
curl -H 'Content-Type: application/json'  -XPOST http://localhost:9200/test_ik_synonym/_search?pretty  -d'
{
    "query" : { "match" : { "content" : "土豆" }},
    "highlight" : {
        "pre_tags" : ["<tag1>", "<tag2>"],
        "post_tags" : ["</tag1>", "</tag2>"],
        "fields" : {
            "content" : {}
        }
    }
}
'

curl -H 'Content-Type: application/json'  -XPOST http://localhost:9200/test_ik_synonym/_search?pretty  -d'
{
    "query" : { "match" : { "content" : "马铃薯" }},
    "highlight" : {
        "pre_tags" : ["<tag1>", "<tag2>"],
        "post_tags" : ["</tag1>", "</tag2>"],
        "fields" : {
            "content" : {}
        }
    }
}
'
~~~

添加同义词列表. 

~~~shell
echo 土豆, 马铃薯 >> ./config/analysis-ik/synonym.txt
cat ./config/analysis-ik/synonym.txt
~~~

然后close, open index. 只有这样才能使得更新的同义词表生效.

~~~shell
curl -X POST "localhost:9200/test_ik_synonym/_close"
curl -X POST "localhost:9200/test_ik_synonym/_open"
~~~

再次查询, 这次土豆和马铃薯可以相互匹配了. 

~~~shell
curl -H 'Content-Type: application/json'  -XPOST http://localhost:9200/test_ik_synonym/_search?pretty  -d'
{
    "query" : { "match" : { "content" : "土豆" }},
    "highlight" : {
        "pre_tags" : ["<tag1>", "<tag2>"],
        "post_tags" : ["</tag1>", "</tag2>"],
        "fields" : {
            "content" : {}
        }
    }
}
'

curl -H 'Content-Type: application/json'  -XPOST http://localhost:9200/test_ik_synonym/_search?pretty  -d'
{
    "query" : { "match" : { "content" : "马铃薯" }},
    "highlight" : {
        "pre_tags" : ["<tag1>", "<tag2>"],
        "post_tags" : ["</tag1>", "</tag2>"],
        "fields" : {
            "content" : {}
        }
    }
}
'
~~~

### 分析

分析以下后台生成的token. 

~~~shell
curl -XPOST 'localhost:9200/test_ik_synonym/_analyze?pretty' -H 'Content-Type: application/json' -d'
{
  "analyzer": "ik_max_word_synonym",
  "text":     "西红柿"
}
'

~~~

返回结果如下: 

~~~shell

{
  "tokens" : [
    {
      "token" : "西红柿",
      "start_offset" : 0,
      "end_offset" : 3,
      "type" : "CN_WORD",
      "position" : 0
    },
    {
      "token" : "番茄",
      "start_offset" : 0,
      "end_offset" : 3,
      "type" : "SYNONYM",
      "position" : 0
    }
  ]
}

~~~

