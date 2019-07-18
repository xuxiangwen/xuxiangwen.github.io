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
    
    curl -XPOST http://localhost:9200/test_ik/_doc/8 -H 'Content-Type:application/json' -d'
    {"content":"我爱天安门\n我爱中国"}
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
   
5.  其他查询

    ~~~shell
    curl -XPOST 'localhost:9200/test_ik/_analyze?pretty' -H 'Content-Type: application/json' -d'
    {
      "analyzer": "ik_smart",
      "text":"相濡以沫的王大爷去世后王奶奶一个人很孤单形影相吊茕茕孑立"
    }
    '
    
    ~~~

6. 添加words和stop_words列表。 添加之前，先看这两个查询。

    词汇: `战66`是一个词汇,  但被分成了两个词`战`和`66`

    ~~~shell
    curl -XPOST 'localhost:9200/test_ik/_analyze?pretty' -H 'Content-Type: application/json' -d'
    {
      "analyzer": "ik_smart",
      "text":"HP的战66笔记本卖的很火"
    }
    '
    
    
    ~~~

    停止词: 下句的关键词是`成功`,  其他词汇都可以去掉

    ~~~shell
    curl -XPOST 'localhost:9200/test_ik/_analyze?pretty' -H 'Content-Type: application/json' -d'
    {
      "analyzer": "ik_smart",
      "text":"归根到底他还是成功了"
    }
    '
    
curl -XPOST 'localhost:9200/test_ik/_analyze?pretty' -H 'Content-Type: application/json' -d'
    {
  "analyzer": "ik_smart",
      "text":"徐湘雯"
    }
    '
    ~~~
    
    如果实现上面说的两种情况呢. 
    
    ~~~shell
    cat << EOF > ./config/analysis-ik/IKAnalyzer.cfg.xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
    <properties>
            <comment>IK Analyzer 扩展配置</comment>
            <!--用户可以在这里配置自己的扩展字典 -->
            <entry key="ext_dict">custom/word.dic</entry>
             <!--用户可以在这里配置自己的扩展停止词字典-->
            <entry key="ext_stopwords">custom/stop_word.dic</entry>
            <!--用户可以在这里配置远程扩展字典 -->
            <!-- <entry key="remote_ext_dict">words_location</entry> -->
            <!--用户可以在这里配置远程扩展停止词字典-->
            <!-- <entry key="remote_ext_stopwords">words_location</entry> -->
    </properties>
    EOF
    cat  ./config/analysis-ik/IKAnalyzer.cfg.xml
    
    mkdir ./config/analysis-ik/custom
    echo 战66 > ./config/analysis-ik/custom/word.dic
    cat ./config/analysis-ik/custom/word.dic

    echo 他 > ./config/analysis-ik/custom/stop_word.dic
echo 归根到底 >> ./config/analysis-ik/custom/stop_word.dic
    echo 还是 >> ./config/analysis-ik/custom/stop_word.dic
    echo 了 >> ./config/analysis-ik/custom/stop_word.dic
    cat ./config/analysis-ik/custom/stop_word.dic
    ~~~
    
重新启动es. 以下命令仅限docker中部署的es. 
    
```shell
    docker stop es-7.2.0
    docker start es-7.2.0
    docker exec -it es-7.2.0 bash
    ```
    
    再次运行上面两个查询, 这次结果符合预期. 
    
    





### 热更新 IK 分词使用方法

目前该插件支持热更新 IK 分词，通过上文在 IK 配置文件中提到的如下配置

```
 	<!--用户可以在这里配置远程扩展字典 -->
	<entry key="remote_ext_dict">location</entry>
 	<!--用户可以在这里配置远程扩展停止词字典-->
	<entry key="remote_ext_stopwords">location</entry>
```

其中 `location` 是指一个 url，比如 `http://yoursite.com/getCustomDict`，该请求只需满足以下两点即可完成分词热更新。

1. 该 http 请求需要返回两个头部(header)，一个是 `Last-Modified`，一个是 `ETag`，这两者都是字符串类型，只要有一个发生变化，该插件就会去抓取新的分词进而更新词库。
2. 该 http 请求返回的内容格式是一行一个分词，换行符用 `\n` 即可。

满足上面两点要求就可以实现热更新分词了，不需要重启 ES 实例。

可以将需自动更新的热词放在一个 UTF-8 编码的 .txt 文件里，放在 nginx 或其他简易 http server 下，当 .txt 文件修改时，http server 会在客户端请求该文件时自动返回相应的 Last-Modified 和 ETag。可以另外做一个工具来从业务系统提取相关词汇，并更新这个 .txt 文件。

