把question-answer数据加载到了多个index中。

- robot3:  ik+synonym+pinyin
- robot2:  ik+synonym
- robot

## robot3: ik+synonym+pinyin

1. 创建index

    ~~~shell
    curl -XDELETE 'localhost:9200/robot3?pretty'
    curl -H 'Content-Type: application/json' -X PUT 'localhost:9200/robot3' -d '
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "ik_max_word_3": { 
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
              "none_chinese_pinyin_tokenize" : false,
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
            "question": {
              "type": "text",
              "analyzer": "ik_max_word_3",
              "search_analyzer": "ik_max_word_3"
            },
            "answer": {
              "type": "text",
              "analyzer": "ik_max_word_3",
              "search_analyzer": "ik_max_word_3"
            },
            "answer_raw": {
              "type": "text",
              "analyzer": "ik_max_word_3",
              "search_analyzer": "ik_max_word_3"
            },
            "category": {
              "type": "text",
              "analyzer": "ik_max_word_3",
              "search_analyzer": "ik_max_word_3"
            },
            "status": {
              "type": "text",
              "analyzer": "ik_max_word_3",
              "search_analyzer": "ik_max_word_3"
            },
            "ask_method": {
              "type": "text",
              "analyzer": "ik_max_word_3",
              "search_analyzer": "ik_max_word_3"
            },
            "match_mode": {
              "type": "text",
              "analyzer": "ik_max_word_3",
              "search_analyzer": "ik_max_word_3"
            },
            "valid_period": {
              "type": "text",
              "analyzer": "ik_max_word_3",
              "search_analyzer": "ik_max_word_3"
            },
            "update_time": {
              "type": "date",
              "format": "YYYY-MM-DD HH:mm:ss"
            }
          }
      }
    }'

    curl 'localhost:9200/robot3/_mapping?pretty=true'   	
    ~~~
    
2. 插入document

    ~~~shell
    # 把数据拷贝到docker映射到本地的目录
    cd /home/grid/eipi10/docker-elk/elasticsearch/data
    cp /home/grid/eipi10/xuxiangwen.github.io/05-ai/40-elasticsearch/data/robot3_knowledgeBase_2018010311371065_20180117.json.gz . 
    gzip -d robot3_knowledgeBase_2018010311371065_20180117.json.gz
    
    curl -H "Content-Type: application/json" -XPOST 'localhost:9200/robot3/_bulk?pretty&refresh' --data-binary "@data/robot3_knowledgeBase_2018010311371065_20180117.json" >  robot2_knowledgeBase_2018010311371065_20180117.log
    curl -XGET 'localhost:9200/robot3/_search?pretty&size=5'            
    
    ~~~

3. 查询拼音`jixing`和`qidong`

   ~~~shell
   # 机型拼音，启动拼音
   curl -XGET 'localhost:9200/robot3/_search?pretty' -H 'Content-Type: application/json' -d'
   {
     "query": {
       "bool": {
         "should": [
           { "match": { "question": "qidong" } },
           { "match": { "question": "jixing" } }
         ]
       }
     }
   }
   '
   ~~~

4. 分析

    ~~~shell
    curl -XPOST 'localhost:9200/robot3/_analyze?pretty' -H 'Content-Type: application/json' -d'
    {
      "analyzer": "ik_max_word_3",
      "text":     "硬盘坏了"
    }
    '
    
    curl -XPOST 'localhost:9200/robot3/_analyze?pretty' -H 'Content-Type: application/json' -d'
    {
      "analyzer": "ik_max_word_3",
      "text":     "固态硬盘"
    }
    '
    ~~~

    

## robot2: ik+synonym

1. 创建index

   ~~~shell
   curl -XDELETE 'localhost:9200/robot2?pretty'
   curl -H 'Content-Type: application/json' -X PUT 'localhost:9200/robot2' -d '
   {
     "settings": {
       "analysis": {
         "analyzer": {
           "ik_max_word_2": { 
             "type": "custom",
             "tokenizer": "ik_max_word",
             "filter": ["ik_synonym_filter"]
           }
         },
         "filter": {
           "ik_synonym_filter": {
             "type": "synonym",
             "synonyms_path": "analysis-ik/synonym.dic"
           }
         }  
       }
     },
     "mappings": {
         "properties": {
           "question": {
             "type": "text",
             "analyzer": "ik_max_word_2",
             "search_analyzer": "ik_max_word_2"
           },
           "answer": {
             "type": "text",
             "analyzer": "ik_max_word_2",
             "search_analyzer": "ik_max_word_2"
           },
           "answer_raw": {
             "type": "text",
             "analyzer": "ik_max_word_2",
             "search_analyzer": "ik_max_word_2"
           },
           "category": {
             "type": "text",
             "analyzer": "ik_max_word_2",
             "search_analyzer": "ik_max_word_2"
           },
           "status": {
             "type": "text",
             "analyzer": "ik_max_word_2",
             "search_analyzer": "ik_max_word_2"
           },
           "ask_method": {
             "type": "text",
             "analyzer": "ik_max_word_2",
             "search_analyzer": "ik_max_word_2"
           },
           "match_mode": {
             "type": "text",
             "analyzer": "ik_max_word_2",
             "search_analyzer": "ik_max_word_2"
           },
           "valid_period": {
             "type": "text",
             "analyzer": "ik_max_word_2",
             "search_analyzer": "ik_max_word_2"
           },
           "update_time": {
             "type": "date",
             "format": "YYYY-MM-DD HH:mm:ss"
           }
         }
     }
   }'
   
   curl 'localhost:9200/robot2/_mapping?pretty=true'   		
   ~~~

2. 插入document

    ```shell
    # 把数据拷贝到docker映射到本地的目录
    cd /home/grid/eipi10/docker-elk/elasticsearch/data/
    cp /home/grid/eipi10/xuxiangwen.github.io/05-ai/40-elasticsearch/data/robot2_knowledgeBase_2018010311371065_20180117.json.gz .
    gzip -d robot2_knowledgeBase_2018010311371065_20180117.json.gz
    
    curl -H "Content-Type: application/json" -XPOST 'localhost:9200/robot2/_bulk?pretty&refresh' --data-binary "@data/robot2_knowledgeBase_2018010311371065_20180117.json" >  robot2_knowledgeBase_2018010311371065_20180117.log
    curl -XGET 'localhost:9200/robot2/_search?pretty&size=5'           
    
    ```

    

3. 查询中文`启动`和`机型`

   无法使用拼音搜索，但可以使用中文。

    ```shell
   curl -XGET 'localhost:9200/robot2/_search?pretty' -H 'Content-Type: application/json' -d'
    {
      "query": {
        "bool": {
          "should": [
            { "match": { "question": "启动" } },
            { "match": { "question": "机型" } }
          ]
        }
      }
    }
   '
    ```

4.  再看同义词。`固态硬盘`和`sd`是同义词, 目前无法实现相互查询. 

     ```shell
    curl -XPOST 'localhost:9200/robot2/_analyze?pretty' -H 'Content-Type: application/json' -d'
    {
        "analyzer": "ik_max_word_2",
        "text":     "固态硬盘"
    }
    '
    
    curl -XPOST 'localhost:9200/robot2/_analyze?pretty' -H 'Content-Type: application/json' -d'
    {
        "analyzer": "ik_max_word_2",
        "text":     "ssd"
    }
    '
     ```

	进行如下设置 .

	```shell
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
	echo 固态硬盘 > ./config/analysis-ik/custom/word.dic
	cat ./config/analysis-ik/custom/word.dic
	
	echo  > ./config/analysis-ik/custom/stop_word.dic
	cat ./config/analysis-ik/custom/stop_word.dic
	
	# 同义词
	touch ./config/analysis-ik/synonym.txt
	echo 固态硬盘, ssd > ./config/analysis-ik/synonym.dic
	cat ./config/analysis-ik/synonym.txt
	```
	
	重新启动es. 以下命令仅限docker中部署的es. 
	
	```shell
	docker stop es-7.2.0
	docker start es-7.2.0
	docker exec -it es-7.2.0 bash
	```
	
	再次运行上面两个查询, 这次结果符合预期. 

## robot: ik

1. 创建index

   ~~~shell
   curl -XDELETE 'localhost:9200/robot?pretty'
   curl -H 'Content-Type: application/json' -X PUT 'localhost:9200/robot' -d '
   {
     "mappings": {
         "properties": {
           "question": {
             "type": "text",
             "analyzer": "ik_max_word",
             "search_analyzer": "ik_max_word"
           },
           "answer": {
             "type": "text",
             "analyzer": "ik_max_word",
             "search_analyzer": "ik_max_word"
           },
           "answer_raw": {
             "type": "text",
             "analyzer": "ik_max_word",
             "search_analyzer": "ik_max_word"
           },
           "category": {
             "type": "text",
             "analyzer": "ik_max_word",
             "search_analyzer": "ik_max_word"
           },
           "status": {
             "type": "text",
             "analyzer": "ik_max_word",
             "search_analyzer": "ik_max_word"
           },
           "ask_method": {
             "type": "text",
             "analyzer": "ik_max_word",
             "search_analyzer": "ik_max_word"
           },
           "match_mode": {
             "type": "text",
             "analyzer": "ik_max_word",
             "search_analyzer": "ik_max_word"
           },
           "valid_period": {
             "type": "text",
             "analyzer": "ik_max_word",
             "search_analyzer": "ik_max_word"
           },
           "update_time": {
             "type": "date",
             "format": "YYYY-MM-DD HH:mm:ss"
           }
         }
     }
   }'
   
   curl 'localhost:9200/robot/_mapping?pretty=true'   		
   ~~~

2. 插入document

   ~~~shell
   # 把数据拷贝到docker映射到本地的目录
   cd /home/grid/eipi10/docker-elk/elasticsearch/data
   cp /home/grid/eipi10/xuxiangwen.github.io/05-ai/40-elasticsearch/data/robot_knowledgeBase_2018010311371065_20180117.json.gz .
   gzip -d robot_knowledgeBase_2018010311371065_20180117.json.gz
   
   curl -H "Content-Type: application/json" -XPOST 'localhost:9200/robot/_bulk?pretty&refresh' --data-binary "@data/robot_knowledgeBase_2018010311371065_20180117.json" >  robot_knowledgeBase_2018010311371065_20180117.log
   curl -XGET 'localhost:9200/robot/_search?pretty&size=5'   
   ~~~

3. 查询

   ~~~shell
   curl -XGET 'localhost:9200/robot/_search?pretty' -H 'Content-Type: application/json' -d'
   {
     "query": {
       "bool": {
         "should": [
           { "match": { "question": "启动" } },
           { "match": { "question": "机型" } }
         ]
       }
     }
   }
   '
   
   curl -XGET 'localhost:9200/robot/_search?pretty' -H 'Content-Type: application/json' -d'
   {
     "query": {
       "bool": {
         "should": [
           { "match": { "question": "驱动更新" } }
         ]
       }
     }
   }
   '
   ~~~

   robot3: ik+synonym+pinyin

   ~~~shell
   curl -XGET 'localhost:9200/robot3/_search?pretty' -H 'Content-Type: application/json' -d'
   {
     "query": {
       "bool": {
         "should": [
           { "match": { "question": "驱动更新" } }
         ]
       }
     }
   }
   '
   
   curl -XGET 'localhost:9200/robot3/_search?pretty' -H 'Content-Type: application/json' -d'
   {
     "query": {
       "query_string": {
         "fields": ["question"],
         "query": "驱动"
       }
     }
   }
   '
   
   curl -XGET 'localhost:9200/robot3/_search?pretty' -H 'Content-Type: application/json' -d'
   {
     "query": {
       "query_string": {
         "fields": ["question"],
         "query": "驱动"
       }
     }
   }
   '
   
   curl -XGET 'localhost:9200/robot3/_search?pretty' -H 'Content-Type: application/json' -d'
   {
     "query": { "match": { "question": "驱动" } }
   }
   '
   
   curl -XGET 'localhost:9200/robot3/_search?pretty' -H 'Content-Type: application/json' -d'
   {
     "query": {
       "query_string": {
         "fields": ["question"],
         "query": "硬盘"
       }
     }
   }
   '
   
   
   ~~~
   
   

