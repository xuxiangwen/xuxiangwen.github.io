# 1. Elastic search介绍

## 1.1 Apache  Lucene介绍

### 架构

- **Document**:  它是在索引和搜索过程中数据的主要表现形式，或者称“载体”，承载着我们索引和搜索的数据,它由一个或者多个域(Field)组成。
- **Field**:   它是Document的组成部分，由两部分组成，名称(name)和值(value)。
- **Term**:  它是搜索的基本单位，其表现形式为文本中的一个词。
- **Token**:  它是单个Term在所属Field中文本的呈现形式，包含了Term内容、Term类型、Term在文本中的起始及偏移位置。

Apache Lucene把所有的信息都写入到一个称为**倒排索引**的数据结构中。这种数据结构把索引中的每个Term与相应的Document映射起来。

假定我们的Document只有title域(Field)被编入索引，Document如下：

- ElasticSearch Servier (document 1)
- Mastering ElasticSearch (document 2)
- Apache Solr 4 Cookbook (document 3)

所以索引(以一种直观的形式)展现如下：

| Term          | count | Docs    |
| ------------- | ----- | ------- |
| 4             | 1     | <3>     |
| Apache        | 1     | <3>     |
| Cookbook      | 1     | <3>     |
| ElasticSearch | 2     | <1> <2> |
| Mastering     | 1     | <1>     |
| Server        | 1     | <1>     |
| Solr          | 1     | <3>     |

