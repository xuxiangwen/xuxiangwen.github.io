## ik中文分词

https://github.com/medcl/elasticsearch-analysis-ik/releases

### 安装

```shell
./bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.2.0/elasticsearch-analysis-ik-7.2.0.zip
```

### 示例

1. 创建index

    ~~~shell
    curl -XDELETE 'localhost:9200/test_ik'
    curl -XPUT 'localhost:9200/test_ik'
    curl -XPOST 'localhost:9200/test_ik/_mapping' -H 'Content-Type:application/json' -d'
    {
            "properties": {
                "content": {
                    "type": "text",
                    "analyzer": "ik_max_word",
                    "search_analyzer": "ik_smart"
                }
            }
    
    }'
    curl -X GET "localhost:9200/_cat/indices?v"
    ~~~

2. 插入document

    ~~~shell
    curl -XPOST http://localhost:9200/test_ik/_doc/1 -H 'Content-Type:application/json' -d'
    {"content":"美国留给伊拉克的是个烂摊子吗"}
    '
    curl -XPOST http://localhost:9200/test_ik/_doc/2 -H 'Content-Type:application/json' -d'
    {"content":"公安部：各地校车将享最高路权"}
    '
    curl -XPOST http://localhost:9200/test_ik/_doc/3 -H 'Content-Type:application/json' -d'
    {"content":"中韩渔警冲突调查：韩警平均每天扣1艘中国渔船"}
    '
    curl -XPOST http://localhost:9200/test_ik/_doc/4 -H 'Content-Type:application/json' -d'
    {"content":"中国驻洛杉矶领事馆遭亚裔男子枪击 嫌犯已自首"}
    '
    curl -XPOST http://localhost:9200/test_ik/_doc/5 -H 'Content-Type:application/json' -d'
    {"content":"中国人民解放军保卫中国"}
    '
    curl -XPOST http://localhost:9200/test_ik/_doc/6 -H 'Content-Type:application/json' -d'
    {"content":"我的女儿非常喜欢吃西红柿炒鸡蛋和清炒土豆丝"}
    '
    curl -XPOST http://localhost:9200/test_ik/_doc/7 -H 'Content-Type:application/json' -d'
    {"content":"我的女儿非常喜欢吃番茄炒鸡蛋和清炒土豆丝"}
    '
    ~~~

3. 查询

    ~~~shell
    curl -XPOST 'localhost:9200/test_ik/_search?pretty'  -H 'Content-Type:application/json' -d'
    {
        "query" : { "match" : { "content" : "中国" }},
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

    ~~~shell
    curl -XPOST 'localhost:9200/test_ik/_search?pretty'  -H 'Content-Type:application/json' -d'
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

4. 比较ik_max_word和ik_smart

   在做搜索引擎的时候, 一般会使用ik_max_word, 这样可以匹配到更多的文档. 然后根据ik_smart分词, 从返回的文档中, 再进行筛选, 选出更加符合的文档. 

   **ik_max_word** : 返回所有分词的可能结果
   
    ~~~shell
    curl -XPOST 'localhost:9200/test_ik/_analyze?pretty' -H 'Content-Type: application/json' -d'
    {
      "analyzer": "ik_max_word",
      "text":     "南京市长江大桥"
    }
 '
    ~~~
   
   输入如下: 
   
   ~~~json
   {
     "tokens" : [
       {
         "token" : "南京市",
         "start_offset" : 0,
         "end_offset" : 3,
         "type" : "CN_WORD",
         "position" : 0
       },
       {
         "token" : "南京",
         "start_offset" : 0,
         "end_offset" : 2,
         "type" : "CN_WORD",
         "position" : 1
       },
       {
         "token" : "市长",
         "start_offset" : 2,
         "end_offset" : 4,
         "type" : "CN_WORD",
         "position" : 2
       },
       {
         "token" : "长江大桥",
         "start_offset" : 3,
         "end_offset" : 7,
         "type" : "CN_WORD",
         "position" : 3
       },
       {
         "token" : "长江",
         "start_offset" : 3,
         "end_offset" : 5,
         "type" : "CN_WORD",
         "position" : 4
       },
       {
         "token" : "大桥",
         "start_offset" : 5,
         "end_offset" : 7,
         "type" : "CN_WORD",
         "position" : 5
       }
     ]
   }
   
   ~~~
   
    **ik_smart** : 返回最有可能的分词结果. 更加简洁. 
   
   ~~~shell
   curl -XPOST 'localhost:9200/test_ik/_analyze?pretty' -H 'Content-Type: application/json' -d'
       {
         "analyzer": "ik_smart",
         "text":     "南京市长江大桥"
       }
       '
   ~~~
   
   输入如下: 
   
   ~~~json
   {
     "tokens" : [
       {
         "token" : "南京市",
         "start_offset" : 0,
         "end_offset" : 3,
         "type" : "CN_WORD",
         "position" : 0
       },
       {
         "token" : "长江大桥",
         "start_offset" : 3,
         "end_offset" : 7,
         "type" : "CN_WORD",
         "position" : 1
       }
     ]
   }
   
   ~~~
   
   

