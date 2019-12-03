## 恢复正式的词库和停用词

~~~hist
cd ll
cp stopword.dic.full stopword.dic
cp word_ext.dic.full word_ext.dic
tail stopword.dic
tail word_ext.dic
~~~

### 进入elastic search container

```shell
docker exec -it `docker ps  | grep elk_elasticsearch | awk '{print $1}'` bash
```

## 数据载入

### KM

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
        "question": {
          "type": "text",
          "analyzer": "ik_max_word_3",
          "search_analyzer": "ik_max_word_3"
        },
        "creator_name": {
          "type": "text"
        }, 
        "modifier_name": {
          "type": "text"
        },
        "create_ts": {
          "type": "date",
          "format": "YYYY-MM-DD HH:mm:ss"
        },
        "modify_ts": {
          "type": "date",
          "format": "YYYY-MM-DD HH:mm:ss"
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
        "latest_star": {
          "type": "float"
        },  
         "click_count_rate": {
          "type": "float"
        },  
         "latest_rate": {
          "type": "float"
        },  
         "search_rate": {
          "type": "float"
        },                
        "category_name": {
          "type": "text",
          "analyzer": "ik_max_word_3",
          "search_analyzer": "ik_max_word_3"
        },
        "primary_category": {
          "type": "text",
          "analyzer": "ik_max_word_3",
          "search_analyzer": "ik_max_word_3"
        },        
        "first_category": {
          "type": "text"
        },        
        "answer": {
          "type": "text",
          "analyzer": "ik_max_word_3",
          "search_analyzer": "ik_max_word_3"
        },
        "html_content": {
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
# 把数据拷贝到docker映射到本地的目录. 需要在docker主机上运行。
# cp /home/grid/eipi10/pp/user_profile/notebook/km_doc.json /home/grid/eipi10/docker-elk/elasticsearch/data/

cd data
curl -X GET 'localhost:9200/_cat/indices?v'	
curl -X POST "localhost:9200/km_doc/_delete_by_query?pretty" -H 'Content-Type: application/json' -d'
{
  "query": { 
    "match_all": {}
  }
}
'

curl -H "Content-Type: application/json" -XPOST 'localhost:9200/km_doc/_bulk?pretty&refresh' --data-binary "@km_doc.json" >  km_doc.log

curl -XGET 'localhost:9200/km_doc/_search?pretty&size=5'  
curl -X GET 'localhost:9200/_cat/indices?v'	
  
# less km_doc.log
~~~

### Case

~~~shell        &quot;primary_category&quot;: {
curl -XDELETE 'localhost:9200/case_qa?pretty'
curl -H 'Content-Type: application/json' -X PUT 'localhost:9200/case_qa' -d '
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
        "case_id": {
          "type": "integer"
        },
        "customer_id": {
          "type": "integer"
        },      
        "session_id": {
          "type": "text"
        },  
        "startsessiontime": {
          "type": "date",
          "format": "YYYY-MM-DD HH:mm:ss"
        },       
        "upgradetype": {
          "type": "text"
        }, 
        "casesource": {
          "type": "text"
        }, 
        "issuetype": {
          "type": "text"
        },        
        "issue_category": {
          "type": "text"
        }, 
        "issue_subcategory": {
          "type": "text"
        },  
        "pn": {
          "type": "text"
        },        
        "producttype": {
          "type": "text"
        }, 
        "productline": {
          "type": "text"
        },       
        "status": {
          "type": "integer"
        },  
        "launchtype": {
          "type": "integer"
        },  
        "casestatus": {
          "type": "integer"
        },          
        "case_days": {
          "type": "integer"
        },  
        "latest_star": {
          "type": "float"
        },  
        "latest_rate": {
          "type": "float"
        },  
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
        "answer_20": {
          "type": "text",
          "analyzer": "ik_max_word_3",
          "search_analyzer": "ik_max_word_3"
        },
        "first_category": {
          "type": "text"       
        } 
      }
  }
}
'

curl 'localhost:9200/case_qa/_mapping?pretty=true'   
~~~

~~~shell

cd data
curl -X GET 'localhost:9200/_cat/indices?v'	
curl -X POST "localhost:9200/case_qa/_delete_by_query?pretty" -H 'Content-Type: application/json' -d'
{
  "query": { 
    "match_all": {}
  }
}
'

curl -H "Content-Type: application/json" -XPOST 'localhost:9200/case_qa/_bulk?pretty&refresh' --data-binary "@case_qa.json" >  case_qa.log

curl -XGET 'localhost:9200/case_qa/_search?pretty&size=5'  
curl -X GET 'localhost:9200/_cat/indices?v'	
  
# less km_doc.log
~~~

## 验证和分析

~~~shell
curl -XGET '15.15.165.218:9200/km_doc/_search?pretty&size=5' -H 'Content-Type: application/json' -d'
{
  "query": {
      "multi_match" : {
      "query" : "Windows 10系统如何安装",
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

curl -XPOST 'localhost:9200/km_doc/_analyze?pretty' -H 'Content-Type: application/json' -d'
{
  "analyzer": "standard",
  "text":     "Printer"
}
'

curl -XPOST 'localhost:9200/km_doc/_analyze?pretty' -H 'Content-Type: application/json' -d'
{
  "analyzer": "standard",
  "text":     "PC Printer"
}
'

curl -XGET '15.15.165.218:9200/km_doc/_search?pretty&size=5' -H 'Content-Type: application/json' -d'
{
      "query": {
        "bool": {
          "should": [
            {
              "match": { 
                "first_category": {
                  "query": "PC Printer",
                  "boost": 1
                }
              }
            }              
          ]
        }        
      }, "size": 3
} 
'

curl -XGET '15.15.165.218:9200/km_doc/_search?pretty&size=5' -H 'Content-Type: application/json' -d'
{
      "query": {
        "bool": {
          "should": [
            {
              "match": { 
                "first_category": {
                  "query": "PC",
                  "boost": 1
                }
              }
            }              
          ]
        }        
      }, "size": 3
} 
'

curl -XGET '15.15.165.218:9200/km_doc/_search?pretty&size=5' -H 'Content-Type: application/json' -d'
{
      "query": {
        "bool": {
          "should": [
            {
              "match": {
                "title": {
                  "query": "电池保养",
                  "boost": 1
                }
              }
            },
            {
              "match": { 
                "content": {
                  "query": "电池保养",
                  "boost": 1
                }
              }
            }           
          ]
        }        
      }, "size": 3
} 
'

curl -XGET '15.15.165.218:9200/km_doc/_search?pretty&size=5' -H 'Content-Type: application/json' -d'
{
      "query": {
        "bool": {
          "should": [
            {
              "match": {
                "title": {
                  "query": "重启",
                  "boost": 1
                }
              }
            },
            {
              "match": { 
                "content": {
                  "query": "重启",
                  "boost": 2
                }
              }
            },
            {
              "match": { 
                "first_category": {
                  "query": "Printer",
                  "boost": 10
                }
              }
            }              
          ]
        }        
      }, "size": 3
} 
'

curl -XGET '15.15.165.218:9200/km_doc/_search?pretty&size=5' -H 'Content-Type: application/json' -d'
{
      "query": {
        "bool": {
          "should": [
            {
              "match": {
                "title": {
                  "query": "机器有触电感",
                  "boost": 1
                }
              }
            },
            {
              "match": { 
                "content": {
                  "query": "机器有触电感",
                  "boost": 1
                }
              }
            },
            {
              "match": { 
                "first_category": {
                  "query": "Printer",
                  "boost": 10
                }
              }
            }              
          ]
        }        
      }, "size": 3
} 
'

curl -XGET '15.15.165.218:9200/km_doc/_search?pretty&size=5' -H 'Content-Type: application/json' -d'
{"query":{"bool":{"should":[{"match":{"question":{"query":"硬盘","boost":1}}},{"match":{"answer":{"query":"硬盘","boost":2}}}]}},"size":100}
'

curl -XPOST '15.15.165.218:9200/km_doc/_search?pretty&size=5' -H 'Content-Type: application/json' -d'
{
	"query": {
		"function_score": {
			"boost_mode": "multiply",
			"field_value_factor": {
				"field": "search_rate"
			},
			"query": {
				"bool": {
					"should": [{
							"match": {
								"Question": {
									"boost": 1,
									"query": "硬盘"
								}
							}
						},
						{
							"match": {
								"Answer": {
									"boost": 2,
									"query": "硬盘"
								}
							}
						}
					]
				}
			}
		}
	},
	"size": 100
}'
~~~

~~~
curl -X POST "localhost:9200/km_doc/_close"
curl -X POST "localhost:9200/km_doc/_open"

curl -XPOST 'localhost:9200/km_doc/_analyze?pretty' -H 'Content-Type: application/json' -d'
{
  "analyzer": "ik_max_word_3",
  "text":     "核显"
}
'

curl -XPOST 'localhost:9200/km_doc/_analyze?pretty' -H 'Content-Type: application/json' -d'
{
  "analyzer": "ik_max_word_3",
  "text":     "传真机"
}
'

curl -XGET '15.15.165.218:9200/km_doc/_search?pretty&size=5' -H 'Content-Type: application/json' -d'
{
  "query": {
    "query_string": {
      "fields": ["title"],
      "query": "核显"
    }
  }
}
'

curl -XGET '15.15.165.218:9200/km_doc/_search?pretty&size=5' -H 'Content-Type: application/json' -d'
{
  "query": {
    "query_string": {
      "fields": ["title"],
      "query": "显卡"
    }
  }
}
'
~~~

