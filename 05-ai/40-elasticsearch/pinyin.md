## 拼音

https://github.com/medcl/elasticsearch-analysis-pinyin

### 安装

```shell
./bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-pinyin/releases/download/v7.2.0/elasticsearch-analysis-pinyin-7.2.0.zip
```

重新启动elasticsearch, 如果在docker的环境中. 把容器stop, 然后start即达到重启的目的.

## 使用pinyin analyzer

1. 创建index

    ~~~shell
    curl -H 'Content-Type: application/json' -X PUT localhost:9200/medcl?pretty -d'
    {
        "settings" : {
            "analysis" : {
                "analyzer" : {
                    "pinyin_analyzer" : {
                        "tokenizer" : "my_pinyin"
                        }
                },
                "tokenizer" : {
                    "my_pinyin" : {
                        "type" : "pinyin",
                        "keep_first_letter":true,                    
                        "keep_separate_first_letter" : false,
                        "keep_full_pinyin" : true,
                        "keep_original" : true,
                        "limit_first_letter_length" : 16,
                        "lowercase" : true,
                        "remove_duplicated_term" : true
                    }
                }
            }
        }
    }'
    curl -X GET "localhost:9200/_cat/indices?v"
    ~~~

2. 测试Analyzer

    ~~~shell
    curl -XPOST 'localhost:9200/medcl/_analyze?pretty' -H 'Content-Type: application/json' -d'
    {
      "analyzer": "pinyin_analyzer",
      "text":     "梅西"
    }
    '
    ~~~

3. 设置属性

    ~~~shell
    curl -H 'Content-Type: application/json'  -XPOST localhost:9200/medcl/_mapping -d'
    {
            "properties": {
                "name": {
                    "type": "keyword",
                    "fields": {
                        "pinyin": {
                            "type": "text",
                            "store": false,
                            "term_vector": "with_offsets",
                            "analyzer": "pinyin_analyzer",
                            "boost": 10
                        }
                    }
                }
            }
    }'
    ~~~

4. 插入document

    ~~~
    curl  -H 'Content-Type: application/json'  -XPOST localhost:9200/medcl/_doc/1 -d'{"name":"刘德华"}'
    curl  -H 'Content-Type: application/json'  -XPOST localhost:9200/medcl/_doc/2-d'{"name":"梅西"}'
    curl  -H 'Content-Type: application/json'  -XPOST localhost:9200/medcl/_doc/3 -d'{"name":"喜欢刘德华的人很多"}'
    curl  -H 'Content-Type: application/json'  -XPOST localhost:9200/medcl/_doc/4 -d'{"name":"他的话很少"}'
    curl  -H 'Content-Type: application/json'  -XPOST localhost:9200/medcl/_doc/5 -d'{"name":"留德华人很多"}'
    curl  -H 'Content-Type: application/json'  -XPOST localhost:9200/medcl/_doc/6 -d'{"name":"非常的伟大梅西"}'
    curl  -H 'Content-Type: application/json'  -XPOST localhost:9200/medcl/_doc/7 -d'{"name":"没戏了"}'
    ~~~

5. 查询

    ~~~shell
    curl -H 'Content-Type: application/json'  -XPOST localhost:9200/medcl/_search?pretty  -d'
    {    "query" : { "match" : { "name" : "刘德华" }}}'
    curl -H 'Content-Type: application/json'  -XPOST localhost:9200/medcl/_search?pretty  -d'
    {    "query" : { "match" : { "name.pinyin" : "刘德" }}}'
    curl -H 'Content-Type: application/json'  -XPOST localhost:9200/medcl/_search?pretty  -d'
    {    "query" : { "match" : { "name.pinyin" : "liu" }}}'
    curl -H 'Content-Type: application/json'  -XPOST localhost:9200/medcl/_search?pretty  -d'
    {    "query" : { "match" : { "name.pinyin" : "ldh" }}}'
    ~~~

    以下是上面几个语句的等效语句.  

    ~~~
    curl -XPOST "localhost:9200/medcl/_search?pretty&q=name:%E5%88%98%E5%BE%B7%E5%8D%8E"
    curl -XPOST "localhost:9200/medcl/_search?pretty&q=name.pinyin:%e5%88%98%e5%be%b7"
    curl -XPOST "localhost:9200/medcl/_search?pretty&q=name.pinyin:liu"
    curl -XPOST "localhost:9200/medcl/_search?pretty&q=name.pinyin:ldh"
    ~~~

## 使用Pinyin-TokenFilter

~~~shell
curl -XDELETE 'localhost:9200/medcl1?pretty'
curl  -H 'Content-Type: application/json'  -XPUT localhost:9200/medcl1/ -d'
{
    "settings" : {
        "analysis" : {
            "analyzer" : {
                "user_name_analyzer" : {
                    "tokenizer" : "whitespace",
                    "filter" : "pinyin_first_letter_and_full_pinyin_filter"
                }
            },
            "filter" : {
                "pinyin_first_letter_and_full_pinyin_filter" : {
                    "type" : "pinyin",
                    "keep_first_letter" : true,
                    "keep_full_pinyin" : false,
                    "keep_joined_full_pinyin" :false,
                    "keep_none_chinese" : true,
                    "keep_original" : false,
                    "none_chinese_pinyin_tokenize" : false,
                    "limit_first_letter_length" : 16,
                    "lowercase" : true,
                    "trim_whitespace" : true,
                    "keep_none_chinese_in_first_letter" : true
                }
            }
        }
    }
}'

curl -X GET "localhost:9200/_cat/indices?v"
~~~

Test: 

~~~shell
curl -XPOST 'localhost:9200/medcl1/_analyze?pretty' -H 'Content-Type: application/json' -d'
{
  "analyzer": "user_name_analyzer",
  "text":     ["刘德华 张学友 郭富城 黎明 四大天王"]
}
'
~~~

## 使用phrase query

创建两个另外两个index, 用来比较不同配置下, analyzer的效果

|                            | medcl | medcl2 | medcl3 |
| -------------------------- | ----- | ------ | ------ |
| keep_first_letter          | true  | false  | false  |
| keep_separate_first_letter | false | false  | true   |
| keep_full_pinyin           | true  | true   | false  |
| keep_joined_full_pinyin    | false | false  | false  |
| keep_original              | true  | false  | false  |

- `keep_first_letter` when this option enabled, eg: `刘德华`>`ldh`, default: true
- `keep_separate_first_letter` when this option enabled, will keep first letters separately, eg: `刘德华`>`l`,`d`,`h`, default: false, NOTE: query result maybe too fuzziness due to term too frequency
- `keep_full_pinyin` when this option enabled, eg: `刘德华`> [`liu`,`de`,`hua`], default: true
- `keep_joined_full_pinyin` when this option enabled, eg: `刘德华`> [`liudehua`], default: false
- `keep_original` when this option enabled, will keep original input as well, default: fals

**步骤**

1. 创建Index

    ~~~shell
    curl -XDELETE 'localhost:9200/medcl2?pretty'
    curl -H 'Content-Type: application/json' -XPUT localhost:9200/medcl2/ -d'
      {
          "settings" : {
              "analysis" : {
                  "analyzer" : {
                      "pinyin_analyzer" : {
                          "tokenizer" : "my_pinyin"
                          }
                  },
                  "tokenizer" : {
                      "my_pinyin" : {
                          "type" : "pinyin",
                          "keep_first_letter":false,
                          "keep_separate_first_letter" : false,
                          "keep_full_pinyin" : true,
                          "keep_original" : false,
                          "limit_first_letter_length" : 16,
                          "lowercase" : true
                      }
                  }
              }
          }
      }
    '

    curl -XDELETE 'localhost:9200/medcl3?pretty'
    curl -H 'Content-Type: application/json' -XPUT localhost:9200/medcl3/ -d'
      {
          "settings" : {
              "analysis" : {
                  "analyzer" : {
                      "pinyin_analyzer" : {
                          "tokenizer" : "my_pinyin"
                          }
                  },
                  "tokenizer" : {
                      "my_pinyin" : {
                          "type" : "pinyin",
                          "keep_first_letter":false,
                          "keep_separate_first_letter" : true,
                          "keep_full_pinyin" : false,
                          "keep_original" : false,
                          "limit_first_letter_length" : 16,
                          "lowercase" : true
                      }
                  }
              }
          }
      }
    '
    
    curl -X GET "localhost:9200/_cat/indices?v"
    ~~~
    
2. 创建mapping

    ~~~shell
    curl -H 'Content-Type: application/json'  -XPOST localhost:9200/medcl2/_mapping -d'
    {
            "properties": {
                "name": {
                    "type": "keyword",
                    "fields": {
                        "pinyin": {
                            "type": "text",
                            "store": false,
                            "term_vector": "with_offsets",
                            "analyzer": "pinyin_analyzer",
                            "boost": 10
                        }
                    }
                }
            }
    }'
    
    curl -H 'Content-Type: application/json'  -XPOST localhost:9200/medcl3/_mapping -d'
    {
            "properties": {
                "name": {
                    "type": "keyword",
                    "fields": {
                        "pinyin": {
                            "type": "text",
                            "store": false,
                            "term_vector": "with_offsets",
                            "analyzer": "pinyin_analyzer",
                            "boost": 10
                        }
                    }
                }
            }
    }'
    ~~~

3. 插入document

    ~~~shell
    curl -H 'Content-Type: application/json' -XPOST localhost:9200/medcl2/_doc/1 -d'{"name":"刘德华"}'
    curl -H 'Content-Type: application/json' -XPOST localhost:9200/medcl2/_doc/2 -d'{"name":"梅西"}'
curl -H 'Content-Type: application/json' -XPOST localhost:9200/medcl2/_doc/3 -d'{"name":"喜欢刘德华的人很多"}'
    curl -H 'Content-Type: application/json' -XPOST localhost:9200/medcl2/_doc/4 -d'{"name":"他的话很少"}'
    curl -H 'Content-Type: application/json' -XPOST localhost:9200/medcl2/_doc/5 -d'{"name":"留德华人很多"}'
    curl -H 'Content-Type: application/json' -XPOST localhost:9200/medcl2/_doc/6 -d'{"name":"非常的伟大梅西"}'
    curl -H 'Content-Type: application/json' -XPOST localhost:9200/medcl2/_doc/7 -d'{"name":"没戏了"}'
    
    curl -H 'Content-Type: application/json' -XPOST localhost:9200/medcl3/_doc/1 -d'{"name":"刘德华"}'
    curl -H 'Content-Type: application/json' -XPOST localhost:9200/medcl3/_doc/2 -d'{"name":"梅西"}'
    curl -H 'Content-Type: application/json' -XPOST localhost:9200/medcl3/_doc/3 -d'{"name":"喜欢刘德华的人很多"}'
    curl -H 'Content-Type: application/json' -XPOST localhost:9200/medcl3/_doc/4 -d'{"name":"他的话很少"}'
    curl -H 'Content-Type: application/json' -XPOST localhost:9200/medcl3/_doc/5 -d'{"name":"留德华人很多"}'
    curl -H 'Content-Type: application/json' -XPOST localhost:9200/medcl3/_doc/6 -d'{"name":"非常的伟大梅西"}'
    curl -H 'Content-Type: application/json' -XPOST localhost:9200/medcl3/_doc/7 -d'{"name":"没戏了"}'
    ~~~
    
4. 分析

   ~~~shell
   curl -XPOST 'localhost:9200/medcl/_analyze?pretty' -H 'Content-Type: application/json' -d'
   {
      "text": ["刘德华"],
      "analyzer": "pinyin_analyzer"
   }
   '
   
   curl -XPOST 'localhost:9200/medcl2/_analyze?pretty' -H 'Content-Type: application/json' -d'
   {
      "text": ["刘德华"],
      "analyzer": "pinyin_analyzer"
   }
   '
   
   curl -XPOST 'localhost:9200/medcl3/_analyze?pretty' -H 'Content-Type: application/json' -d'
   {
      "text": ["刘德华"],
      "analyzer": "pinyin_analyzer"
   }
   '
   
   
   ~~~

5. 查询比较结果

   奇怪, 官方的几个例子都不能正常工作, 感觉pinyin作为tokenizer, 可能真的不太合适. 
   
   ~~~shell
   curl -H 'Content-Type: application/json'  -XPOST http://localhost:9200/medcl/_search?pretty  -d'
   {    
     "query" : { 
       "match_phrase" : { "name.pinyin" : "刘德华" }
     }
   }'
   
   curl -H 'Content-Type: application/json'  -XPOST http://localhost:9200/medcl/_search?pretty  -d'
   {    
     "query" : { 
       "match_phrase" : { "name.pinyin" : "梅西" }
     }
   }'
   
   curl -H 'Content-Type: application/json'  -XPOST http://localhost:9200/medcl/_search?pretty  -d'
   {    
     "query" : { 
       "match_phrase" : { "name.pinyin" : "mx" }
     }
   }'
   
   
   
   curl -H 'Content-Type: application/json'  -XPOST localhost:9200/medcl/_search?pretty  -d'
   {    "query" : { "match" : { "name.pinyin" : "liu" }}}'
   
   curl -H 'Content-Type: application/json'  -XPOST http://localhost:9200/medcl2/_search?pretty  -d'
   {    
     "query" : { 
       "match_phrase" : { "name.pinyin" : "刘德华" }
     }
   }'
   
   curl -H 'Content-Type: application/json'  -XPOST http://localhost:9200/medcl3/_search?pretty  -d'
   {    
     "query" : { 
       "match_phrase" : { "name.pinyin" : "刘德华" }
     }
   }'
   ~~~
   
   ~~~shell
   curl -H 'Content-Type: application/json'  -XPOST http://localhost:9200/medcl/_search?pretty  -d'
   {    
     "query" : { 
       "match_phrase" : { "name.pinyin" : "刘dh" }
     }
   }'
   
   curl -H 'Content-Type: application/json'  -XPOST http://localhost:9200/medcl2/_search?pretty  -d'
   {    
     "query" : { 
       "match_phrase" : { "name.pinyin" : "刘dh" }
     }
   }'
   
   curl -H 'Content-Type: application/json'  -XPOST http://localhost:9200/medcl3/_search?pretty  -d'
   {    
     "query" : { 
       "match_phrase" : { "name.pinyin" : "刘dh" }
     }
   }'
   ~~~
   
   