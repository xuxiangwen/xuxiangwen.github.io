

## 数据载入

~~~shell
curl -XDELETE 'localhost:9200/km_doc?pretty'
curl -H 'Content-Type: application/json' -X PUT 'localhost:9200/km_doc' -d '
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
        "doc_id": {
          "type": "integer"
        },
        "title": {
          "type": "text",
          "analyzer": "ik_max_word_3",
          "search_analyzer": "ik_max_word_3"
        },
        "creator_name": {
          "type": "text"
        },
        "create_ts": {
          "type": "date",
          "format": "YYYY-MM-DD HH:mm:ss"
        },    
        "modifier_name": {
          "type": "text"
        }, 
        "status_ts": {
          "type": "date",
          "format": "YYYY-MM-DD HH:mm:ss"
        }, 
        "click_count": {
          "type": "float"
        },
        "click_count_decay": {
          "type": "float"
        },     
        "click_count_decay_star": {
          "type": "float"
        },         
        "category_name": {
          "type": "text",
          "analyzer": "ik_max_word_3",
          "search_analyzer": "ik_max_word_3"
        },
        "content": {
          "type": "text",
          "analyzer": "ik_max_word_3",
          "search_analyzer": "ik_max_word_3"
        }
      }
  }
}
'

curl 'localhost:9200/km_doc/_mapping?pretty=true'   	
~~~



~~~shell
# 把数据拷贝到docker映射到本地的目录
cp /home/grid/eipi10/pp/user_profile/notebook/km_doc.json /home/grid/eipi10/docker-elk/elasticsearch/data/

curl -H "Content-Type: application/json" -XPOST 'localhost:9200/km_doc/_bulk?pretty&refresh' --data-binary "@data/km_doc.json" >  km_doc.log

curl -XGET 'localhost:9200/km_doc/_search?pretty&size=5'  
curl -X GET 'localhost:9200/_cat/indices?v'	
~~~



## 验证和分析

~~~shell
curl -XGET '15.15.165.218:9200/km_doc/_search?pretty&size=5' -H 'Content-Type: application/json' -d'
{
  "query": {
      "multi_match" : {
      "query" : "电池保养",
      "fields": ["title", "content"]
      }
  }
}
'

curl -XGET '15.15.165.218:9200/km_doc/_search?pretty&size=5' -H 'Content-Type: application/json' -d'
{
  "query": {
      "multi_match" : {
      "query" : "电池保养",
      "fields": ["title"]
      }
  }
}
'

curl -XGET '15.15.165.218:9200/km_doc/_search?pretty&size=5' -H 'Content-Type: application/json' -d'
{
  "query": {
    "query_string": {
      "fields": ["title"],
      "query": "电池保养"
    }
  }
}
'

curl -XGET '15.15.165.218:9200/km_doc/_search?pretty&size=5' -H 'Content-Type: application/json' -d'
{
  "query": {
    "query_string": {
      "fields": ["title"],
      "query": "电池保养"
    }
  }
}
'

curl -XPOST 'localhost:9200/km_doc/_analyze?pretty' -H 'Content-Type: application/json' -d'
{
  "analyzer": "ik_max_word_3",
  "text":     "电池保养"
}
'

curl -XPOST 'localhost:9200/km_doc/_analyze?pretty' -H 'Content-Type: application/json' -d'
{
  "analyzer": "ik_max_word_3",
  "text":     "如果用力过猛，有可能会坏"
}
'

# 同义词 存食
curl -XPOST 'localhost:9200/km_doc/_analyze?pretty' -H 'Content-Type: application/json' -d'
{
  "analyzer": "ik_max_word_3",
  "text":     "食积"
}
'

# 自定义词汇 存食
curl -XPOST 'localhost:9200/km_doc/_analyze?pretty' -H 'Content-Type: application/json' -d'
{
  "analyzer": "ik_max_word_3",
  "text":     "徐湘雯"
}
'



~~~



## 人工维护

