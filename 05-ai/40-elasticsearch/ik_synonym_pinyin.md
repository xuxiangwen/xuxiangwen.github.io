## 创建index

~~~ shell
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
    "query" : { "match" : { "content" : "我的女儿" }},
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

其中最后一个查询，定位到了了`我`这个字。 

~~~json
{
  "took" : 7,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 0.23090068,
    "hits" : [
      {
        "_index" : "test_ik_synonym_pinyin",
        "_type" : "_doc",
        "_id" : "2",
        "_score" : 0.23090068,
        "_source" : {
          "content" : "我的女儿非常喜欢吃番茄炒鸡蛋和清炒马铃薯丝"
        },
        "highlight" : {
          "content" : [
            "<tag1>我</tag1>的女儿非常喜欢吃番茄炒鸡蛋和清炒马铃薯丝"
          ]
        }
      },
      {
        "_index" : "test_ik_synonym_pinyin",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 0.22753258,
        "_source" : {
          "content" : "我的女儿非常喜欢吃西红柿炒鸡蛋和清炒土豆丝"
        },
        "highlight" : {
          "content" : [
            "<tag1>我</tag1>的女儿非常喜欢吃西红柿炒鸡蛋和清炒土豆丝"
          ]
        }
      }
    ]
  }
}

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

