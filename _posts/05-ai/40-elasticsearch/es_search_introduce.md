# es查询入门

对elastic search的查询入门, 可以从本文开始.  本文的内容来自[Elasticsearch  Gettting Started](https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html). 

## 加载1000条示例数据

数据是[json-generator](http://www.json-generator.com/)里产出的.

~~~shell
wget -O  accounts.json https://github.com/elastic/elasticsearch/blob/master/docs/src/test/resources/accounts.json?raw=true

curl -H "Content-Type: application/json" -XPOST "localhost:9200/bank/_bulk?pretty&refresh" --data-binary "@accounts.json"
curl "localhost:9200/_cat/indices?v"

~~~

## Search API

有两种方式. 一般都采用第二种方式, 这时由于该方式采用json来编写, 拥有超强的表达能力. 

- [REST request URI](https://www.elastic.co/guide/en/elasticsearch/reference/7.2/search-uri-request.html)

  ~~~shell
  # 返回4个document
  curl -X GET "localhost:9200/bank/_search?q=*&sort=account_number:asc&pretty&size=4"
  ~~~

- [REST request body](https://www.elastic.co/guide/en/elasticsearch/reference/7.2/search-request-body.html)

  等价脚本.  注意`size`的默认值是10

  ~~~shell
  curl -X GET "localhost:9200/bank/_search?pretty" -H 'Content-Type: application/json' -d'
  {
    "query": { "match_all": {} },
    "sort": [
      { "account_number": "asc" }
    ],
    "size": 4
  }
  '
  ~~~

## 执行查询

**指定返回字段**

~~~shell
curl -X GET "localhost:9200/bank/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": { "match_all": {} },
  "_source": ["account_number", "balance"],
   "size": 4
}
'

~~~

**查询acccount number等于20**

~~~shell
curl -X GET "localhost:9200/bank/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": { "match": { "account_number": 20 } }
}
'

~~~

**查询address中包含mill**

匹配默认是忽略大小写的. 

~~~shell
curl -X GET "localhost:9200/bank/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": { "match": { "address": "mill" } }
}
'
~~~

**查询address中包含mill或者street**

~~~shell
curl -X GET "localhost:9200/bank/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": { "match": { "address": "mill street" } }
}
'

# 同上
curl -X GET "localhost:9200/bank/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "should": [
        { "match": { "address": "mill" } },
        { "match": { "address": "street" } }
      ]
    }
  }
}
'

~~~

**查询address包含`mill lane`短语的**

~~~shell
curl -X GET "localhost:9200/bank/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": { "match_phrase": { "address": "mill lane" } }
}
'
~~~

**查询address中同时包含mill和lane**

~~~shell
curl -X GET "localhost:9200/bank/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": [
        { "match": { "address": "mill" } },
        { "match": { "address": "lane" } }
      ]
    }
  }
}
'
~~~

**查询address中不能包含mill或lane**

~~~shell
curl -X GET "localhost:9200/bank/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must_not": [
        { "match": { "address": "mill" } },
        { "match": { "address": "lane" } }
      ]
    }
  }
}
'

~~~

**查询age是40,但是state不等于ID**

~~~shell
curl -X GET "localhost:9200/bank/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": [
        { "match": { "age": "40" } }
      ],
      "must_not": [
        { "match": { "state": "ID" } }
      ]
    }
  }
}
'

~~~

## 执行过滤`Filter`

~~~shell
curl -X GET "localhost:9200/bank/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": { "match_all": {} },
      "filter": {
        "range": {
          "balance": {
            "gte": 20000,
            "lte": 30000
          }
        }
      }
    }
  },
  "size": 2
}
'
~~~

## 执行 Aggregation

**group by state**

~~~shell
curl -X GET "localhost:9200/bank/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "group_by_state": {
      "terms": {
        "field": "state.keyword"
      }
    }
  }
}
'

~~~

上面的语句等效于:

~~~sql
SELECT state, COUNT(*) FROM bank GROUP BY state ORDER BY COUNT(*) DESC LIMIT 10;
~~~

**group by state, avg(balance)**

~~~shell
curl -X GET "localhost:9200/bank/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "group_by_state": {
      "terms": {
        "field": "state.keyword"
      },
      "aggs": {
        "average_balance": {
          "avg": {
            "field": "balance"
          }
        }
      }
    }
  }
}
'

~~~

**group by state, avg(balance), sort by state**

~~~shell
curl -X GET "localhost:9200/bank/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "group_by_state": {
      "terms": {
        "field": "state.keyword",
        "order": {
          "average_balance": "desc"
        }
      },
      "aggs": {
        "average_balance": {
          "avg": {
            "field": "balance"
          }
        }
      }
    }
  }
}
'

~~~

**age brackets (ages 20-29, 30-39, and 40-49), then by gender, avg(balance)**

~~~shell
curl -X GET "localhost:9200/bank/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "group_by_age": {
      "range": {
        "field": "age",
        "ranges": [
          {
            "from": 20,
            "to": 30
          },
          {
            "from": 30,
            "to": 40
          },
          {
            "from": 40,
            "to": 50
          }
        ]
      },
      "aggs": {
        "group_by_gender": {
          "terms": {
            "field": "gender.keyword"
          },
          "aggs": {
            "average_balance": {
              "avg": {
                "field": "balance"
              }
            }
          }
        }
      }
    }
  }
}
'

~~~

