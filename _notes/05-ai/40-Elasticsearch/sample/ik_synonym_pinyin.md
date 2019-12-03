# ik中文分词 +  同义词Synonym  + 拼音

## 进入elastic search container

~~~shell
docker exec -it `docker ps  | grep elk_elasticsearch | awk '{print $1}'` bash
~~~

## 创建index

~~~ shell
curl -X DELETE "localhost:9200/test_ik_synonym_pinyin?pretty"
curl -XPUT 'localhost:9200/test_ik_synonym_pinyin?pretty' -H 'Content-Type: application/json' -d'
{
  "settings": {
    "analysis": {
      "analyzer": {
        "ik_max_word_synonym_pinyin": { 
          "type": "custom",
          "tokenizer": "ik_max_word",
          "filter": ["ik_synonym_filter", "ik_pinyin_filter"]
        }
      },
      "filter": {
        "ik_synonym_filter": {
          "type": "synonym",
          "synonyms_path": "analysis-ik/synonym.dic"
        },
        "ik_pinyin_filter" : {
          "type" : "pinyin",
          "keep_first_letter" : false,
          "keep_full_pinyin" : false,
          "keep_joined_full_pinyin" :true,
          "keep_none_chinese" : true,
          "keep_original" : true,
          "limit_first_letter_length" : 16,
          "lowercase" : true,
          "trim_whitespace" : true,
          "keep_none_chinese_in_first_letter" : true
        }
      }  
    }
  },
  "mappings": {
      "properties": {
        "content": {
          "type": "text",
          "analyzer": "ik_max_word_synonym_pinyin",
          "search_analyzer": "ik_max_word_synonym_pinyin"
        }
      }
  }
}
'

curl -XGET 'localhost:9200/test_ik_synonym_pinyin?pretty'
~~~

## 插入document

~~~shell
curl -H 'Content-Type: application/json'  -XPOST localhost:9200/test_ik_synonym_pinyin/_doc/1?pretty -d'
{"content":"我的女儿非常喜欢吃西红柿炒鸡蛋和清炒土豆丝"}
'
curl -H 'Content-Type: application/json'  -XPOST localhost:9200/test_ik_synonym_pinyin/_doc/2?pretty -d'
{"content":"我的女儿非常喜欢吃番茄炒鸡蛋和清炒马铃薯丝"}
'
~~~

## 查询数据

### 同义词

西红柿和番茄，土豆和马铃薯，这两对同义词已经在[ik中文分词 +  同义词Synonym ](ik_synonym.md)中加入了。所以下面的每个查询都能匹配两条语句。

~~~shell
curl -H 'Content-Type: application/json'  -XPOST localhost:9200/test_ik_synonym_pinyin/_search?pretty  -d'
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

curl -H 'Content-Type: application/json'  -XPOST localhost:9200/test_ik_synonym_pinyin/_search?pretty  -d'
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
~~~

### 拼音

以下两个查询返回相同的结果。

~~~shell
curl -H 'Content-Type: application/json'  -XPOST localhost:9200/test_ik_synonym_pinyin/_search?pretty  -d'
{
    "query" : { "match" : { "content" : "女儿" }},
    "highlight" : {
        "pre_tags" : ["<tag1>", "<tag2>"],
        "post_tags" : ["</tag1>", "</tag2>"],
        "fields" : {
            "content" : {}
        }
    }
}
'

curl -H 'Content-Type: application/json'  -XPOST localhost:9200/test_ik_synonym_pinyin/_search?pretty  -d'
{
    "query" : { "match" : { "content" : "nver" }},
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

~~~shell
curl -XPOST 'localhost:9200/test_ik_synonym_pinyin/_analyze?pretty' -H 'Content-Type: application/json' -d'
{
  "analyzer": "ik_max_word_synonym_pinyin",
  "text":     "西红柿"
}
'

curl -XPOST 'localhost:9200/test_ik_synonym_pinyin/_analyze?pretty' -H 'Content-Type: application/json' -d'
{
  "analyzer": "ik_max_word_synonym_pinyin",
  "text":     "我爱吃马铃薯"
}
'

curl -XPOST 'localhost:9200/test_ik_synonym_pinyin/_analyze?pretty' -H 'Content-Type: application/json' -d'
{
  "analyzer": "ik_max_word_synonym_pinyin",
  "text":     "fanqie"
}
'

curl -XPOST 'localhost:9200/test_ik_synonym_pinyin/_analyze?pretty' -H 'Content-Type: application/json' -d'
{
  "analyzer": "ik_max_word_synonym_pinyin",
  "text":     "反切"
}
'

curl -XPOST 'localhost:9200/test_ik_synonym_pinyin/_analyze?pretty' -H 'Content-Type: application/json' -d'
{
  "analyzer": "ik_max_word_synonym_pinyin",
  "text":     "wodenver"
}
'
~~~

其中最后一个分析，揭示了为何上节最后一个查询，定位到了`我。下面第二个token是`den`, 这实际上是一个pinyin filter的错误。 

~~~json
{
  "tokens" : [
    {
      "token" : "wo",
      "start_offset" : 0,
      "end_offset" : 8,
      "type" : "ENGLISH",
      "position" : 0
    },
    {
      "token" : "den",
      "start_offset" : 0,
      "end_offset" : 8,
      "type" : "ENGLISH",
      "position" : 1
    },
    {
      "token" : "v",
      "start_offset" : 0,
      "end_offset" : 8,
      "type" : "ENGLISH",
      "position" : 2
    },
    {
      "token" : "er",
      "start_offset" : 0,
      "end_offset" : 8,
      "type" : "ENGLISH",
      "position" : 3
    },
    {
      "token" : "wodenver",
      "start_offset" : 0,
      "end_offset" : 8,
      "type" : "ENGLISH",
      "position" : 3
    }
  ]
}

~~~

而我的女儿分析中， 也会有`wo`。

~~~shell
curl -XPOST 'localhost:9200/test_ik_synonym_pinyin/_analyze?pretty' -H 'Content-Type: application/json' -d'
{
  "analyzer": "ik_max_word_synonym_pinyin",
  "text":     "我的女儿"
}
'
~~~

返回如下：

~~~json
{
  "tokens" : [
    {
      "token" : "我",
      "start_offset" : 0,
      "end_offset" : 1,
      "type" : "CN_CHAR",
      "position" : 0
    },
    {
      "token" : "wo",
      "start_offset" : 0,
      "end_offset" : 1,
      "type" : "CN_CHAR",
      "position" : 0
    },
    {
      "token" : "的",
      "start_offset" : 1,
      "end_offset" : 2,
      "type" : "CN_CHAR",
      "position" : 1
    },
    {
      "token" : "de",
      "start_offset" : 1,
      "end_offset" : 2,
      "type" : "CN_CHAR",
      "position" : 1
    },
    {
      "token" : "女儿",
      "start_offset" : 2,
      "end_offset" : 4,
      "type" : "CN_WORD",
      "position" : 2
    },
    {
      "token" : "nver",
      "start_offset" : 2,
      "end_offset" : 4,
      "type" : "CN_WORD",
      "position" : 2
    }
  ]
}

~~~

