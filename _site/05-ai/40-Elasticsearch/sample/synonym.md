## Synonym Token Filter

https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-synonym-tokenfilter.html

同义词Token Filter.  采用人工定义同义词列表来进行同义词匹配.

**创建index,  并定义analyzer**

```shell
curl -X DELETE "localhost:9200/test_synonym?pretty"
curl -X PUT "localhost:9200/test_synonym?pretty" -H 'Content-Type: application/json' -d'
{
    "settings": {
        "index" : {
            "analysis" : {
                "analyzer" : {
                    "synonym" : {
                        "tokenizer" : "whitespace",
                        "filter" : ["synonym"]
                    }
                },
                "filter" : {
                    "synonym" : {
                        "type" : "synonym",
                        "synonyms_path" : "analysis/synonym.dic"
                    }
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "content": {
                "type": "text",
                "analyzer": "synonym",
                "search_analyzer": "synonym"
            }
        }  
    }
}
'
curl -X GET "localhost:9200/_cat/indices?v"
```

**创建同义词列表**

```shell
cat > ./config/analysis/synonym.dic << EOF 
# Blank lines and lines starting with pound are comments.

# Explicit mappings match any token sequence on the LHS of "=>"
# and replace with all alternatives on the RHS.  These types of mappings
# ignore the expand parameter in the schema.
# Examples:
i-pod, i pod => ipod,
sea biscuit, sea biscit => seabiscuit

# Equivalent synonyms may be separated with commas and give
# no explicit mapping.  In this case the mapping behavior will
# be taken from the expand parameter in the schema.  This allows
# the same synonym file to be used in different synonym handling strategies.
# Examples:
ipod, i-pod, i pod
foozball , foosball
universe , cosmos
lol, laughing out loud

# If expand==true, "ipod, i-pod, i pod" is equivalent
# to the explicit mapping:
ipod, i-pod, i pod => ipod, i-pod, i pod
# If expand==false, "ipod, i-pod, i pod" is equivalent
# to the explicit mapping:
ipod, i-pod, i pod => ipod

# Multiple synonym mapping entries are merged.
foo => foo bar
foo => baz
# is equivalent to
foo => foo bar, baz

EOF

head ./config/analysis/synonym.dic
```

**close, open index**

只有这样才能使得更新的同义词表生效.

```shell
curl -X POST "localhost:9200/test_synonym/_close"
curl -X POST "localhost:9200/test_synonym/_open"
```

再次查询, 这次土豆和马铃薯可以相互匹配了. 

**插入document**

```shell
curl -XPOST http://localhost:9200/test_synonym/_doc/1?pretty -H 'Content-Type:application/json' -d'
{"content":"i like ipod"}
'

curl -XPOST http://localhost:9200/test_synonym/_doc/2?pretty -H 'Content-Type:application/json' -d'
{"content":"i like i-pod"}
'
```

**查询**

```shell
curl -XPOST 'localhost:9200/test_synonym/_search?pretty'  -H 'Content-Type:application/json' -d'
{
    "query" : { "match" : { "content" : "i-pod" }},
    "highlight" : {
        "pre_tags" : ["<tag1>", "<tag2>"],
        "post_tags" : ["</tag1>", "</tag2>"],
        "fields" : {
            "content" : {}
        }
    }
}
'

curl -XPOST 'localhost:9200/test_synonym/_search?pretty'  -H 'Content-Type:application/json' -d'
{
    "query" : { "match" : { "content" : "ipod" }},
    "highlight" : {
        "pre_tags" : ["<tag1>", "<tag2>"],
        "post_tags" : ["</tag1>", "</tag2>"],
        "fields" : {
            "content" : {}
        }
    }
}
'

```

**清理**

~~~shell
rm -rf ./config/analysis/synonym.dic
~~~

