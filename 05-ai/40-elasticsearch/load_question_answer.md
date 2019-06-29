把question-answer数据加载到了多个index中。

- robot3:  ik+synonym+pinyin
- robot2:  ik+synonym
- robot

## Load question-answer: ik+synonym+pinyin

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
              "synonyms_path": "analysis-ik/synonym.txt"
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
    curl -H "Content-Type: application/json" -XPOST 'localhost:9200/robot3/_bulk?pretty&refresh' --data-binary "@data/robot3_knowledgeBase_2018010311371065_20180117.json" >  robot2_knowledgeBase_2018010311371065_20180117.log
    curl -XGET 'localhost:9200/robot3/_search?pretty&size=5'            
    
    ~~~

3. 查询拼音`jixing`和`qidong`

   ~~~
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

   

## Load question-answer: ik+synonym

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
             "synonyms_path": "analysis-ik/synonym.txt"
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
    curl -H "Content-Type: application/json" -XPOST 'localhost:9200/robot3/_bulk?pretty&refresh' --data-binary "@data/robot2_knowledgeBase_2018010311371065_20180117.json" >  robot2_knowledgeBase_2018010311371065_20180117.log
    curl -XGET 'localhost:9200/robot3/_search?pretty&size=5'            

    ```

3. 查询拼音`jixing`和`qidong`

   ```shell
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
   ```

   

