## **Insurance** 

https://github.com/Samurais/insuranceqa-corpus-zh 

保险领域的中文问答. 

1. 创建index

   ~~~shell
   curl -H 'Content-Type: application/json' -X PUT 'localhost:9200/insurance' -d '
   {
     "mappings": {
         "properties": {
           "question_id": {
             "type": "long"
           },
           "question": {
             "type": "text",
             "analyzer": "ik_max_word",
             "search_analyzer": "ik_max_word"
           },
           "answer": {
             "type": "text",
             "analyzer": "ik_max_word",
             "search_analyzer": "ik_max_word"
           }
         }
     }
   }'
   
   ~~~
   
2. 插入document

   ~~~shell
   # 把数据拷贝到docker映射到本地的目录
   cp /home/grid/eipi10/xuxiangwen.github.io/05-ai/40-elasticsearch/data/insuranceqa.json.gz /home/grid/eipi10/elasticsearch/data
   gzip -d /home/grid/eipi10/elasticsearch/data/insuranceqa.json.gz
   
   curl -H "Content-Type: application/json" -XPOST 'localhost:9200/insurance/_bulk?pretty&refresh' --data-binary "@data/insuranceqa.json" >  insuranceqa.log
   curl -XGET 'localhost:9200/insurance/_search?pretty&size=5'   
   
   cd 
   ~~~

   

3. 查询

   ~~~shell
   curl -XGET 'localhost:9200/insurance/_search?pretty' -H 'Content-Type: application/json' -d'
   {
     "query": {
       "bool": {
         "should": [
           { "match": { "question": "生命" } },
           { "match": { "question": "现金" } }
         ]
       }
     }
   }
   '
   ~~~

   

4. sdsd

5. we

6. we