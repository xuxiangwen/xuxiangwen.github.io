

## Corpora 和 Vector Spaces

参考[Core Concepts](https://radimrehurek.com/gensim/auto_examples/core/run_core_concepts.html)，[Corpora and Vector Spaces](https://tedboy.github.io/nlps/gensim_tutorial/tut1.html)。

### 文档（Document）

一段字符串。

~~~python
document = "Human machine interface for lab abc computer applications"
~~~

### 语料库（Corpus）

Corpus指一组Document。

- 原始

    ~~~python
    text_corpus = [
        "Human machine interface for lab abc computer applications",
        "A survey of user opinion of computer system response time",
        "The EPS user interface management system",
        "System and human system engineering testing of EPS",
        "Relation of user perceived response time to error measurement",
        "The generation of random binary unordered trees",
        "The intersection graph of paths in trees",
        "Graph minors IV Widths of trees and well quasi ordering",
        "Graph minors A survey",
    ]
    ~~~

- 基本处理

  一般的行为有：

  - 分词：对于英文来说，相对比较简单，而对于中文则复杂的多。
  - 去除stopwords
  - 删除低频词

  ~~~python
  from pprint import pprint
  
  # Create a set of frequent words
  stoplist = set('for a of the and to in'.split(' '))
  # Lowercase each document, split it by white space and filter out stopwords
  texts = [[word for word in document.lower().split() if word not in stoplist]
           for document in text_corpus]
  
  # Count word frequencies
  from collections import defaultdict
  frequency = defaultdict(int)
  for text in texts:
      for token in text:
          frequency[token] += 1
  
  # Only keep words that appear more than once
  processed_corpus = [[token for token in text if frequency[token] > 1] for text in texts]
  pprint(processed_corpus)
  ~~~

  ![image-20200609082203231](images/image-20200609082203231.png)-

  对于中文，可以类似这样处理。其中分词采用了[jieba](https://github.com/fxsjy/jieba)。

  ~~~shell
  import jieba
  import urllib
  from pprint import pprint
  
  # 下载停用词
  response = urllib.request.urlopen('https://raw.githubusercontent.com/goto456/stopwords/master/cn_stopwords.txt')
  stop_words = [str(word[:-1],'utf-8') for word in response.readlines()]
  
  docs =  ['自然语言处理是计算机科学领域与人工智能领域中的一个重要方向。',
       '它研究能实现人与计算机之间用自然语言进行有效通信的各种理论和方法。',
       '自然语言处理是一门融语言学、计算机科学、数学于一体的科学。',
       '因此，这一领域的研究将涉及自然语言，即人们日常使用的语言，',
       '所以它与语言学的研究有着密切的联系，但又有重要的区别。',
       '自然语言处理并不是一般地研究自然语言，',
       '而在于研制能有效地实现自然语言通信的计算机系统，',
       '特别是其中的软件系统。因而它是计算机科学的一部分。']
  
  corpus = [[word for word in jieba.cut(doc) if word not in stop_words] for doc in docs ]
  pprint(corpus)
  ~~~

  ![image-20200609084113301](images/image-20200609084113301.png)

- 向量化

  基本处理后，再把语料库用向量的形式来表达，详见下一节。

### 向量（Vector）

为了能够便于Model的调用，还需要把语料库用向量的形式来表示。而向量化，也意味着语料所占空间大大减少，这样就能处理更大的语料库。

#### 字典（Dictionary）

首先要构建Dictionary，即创建gensim.corpora.dictionary.Dictionary类。

~~~python
from gensim import corpora

dictionary = corpora.Dictionary(processed_corpus)
print(dictionary)
~~~

![image-20200609085338894](images/image-20200609085338894.png)

Dictionary非常有用，它的详细描述如下。

- Attributes
  - id2token：Reverse mapping for token2id, initialized in a lazy manner to save memory (not created until needed).
  - token2id：token -> tokenId。
  - cfs： 每个token出现的频次。
  - dfs：每个token出现在多少个文档中。
  - num_nnz：每篇文档unique word的个数汇总。
  - num_docs： 文档数量。
  - num_pos：总共多少个word。
- Methods
  - doc2bow：把文档转化为BOW格式

下面通过一个简单的例子来体验这些属性和方法。

~~~python
from gensim.corpora.dictionary import Dictionary
docs = [
    ["black", "cat", "white", "cat"],
    ["cat", "outer", "space", "cat"],
    ["wag", "dog"]
]

from gensim.corpora.dictionary import Dictionary
dict = Dictionary(docs)

# 由于id2token是lazy manner， 所以先调用任何一个元素，触发生成id2token
print(dict[0])
print("dict.id2token =", dict.id2token)   
print('-'*50)
print("dict.token2id =", dict.token2id)
print('-'*50)
print("dict.cfs =", dict.cfs)			
print('-'*50)
print("dict.dfs =", dict.dfs)			# 
print('-'*50)
print("dict.num_nnz =", dict.num_nnz)
print('-'*50)
print("dict.num_docs =", dict.num_docs)
print('-'*50)
print("dict.num_pos =", dict.num_pos)
print('-'*50)

print("dict.doc2bow(docs[0]) =", dict.doc2bow(docs[0]))
print('-'*50)
print("dict.doc2idx(docs[0]) =", dict.doc2idx(docs[0]))
print('-'*50)
~~~

结果如下：

~~~shell
black
dict.id2token = {0: 'black', 1: 'cat', 2: 'white', 3: 'outer', 4: 'space', 5: 'dog', 6: 'wag'}
--------------------------------------------------
dict.token2id = {'black': 0, 'cat': 1, 'white': 2, 'outer': 3, 'space': 4, 'dog': 5, 'wag': 6}
--------------------------------------------------
dict.cfs = {0: 1, 1: 4, 2: 1, 3: 1, 4: 1, 6: 1, 5: 1}
--------------------------------------------------
dict.dfs = {0: 1, 1: 2, 2: 1, 3: 1, 4: 1, 6: 1, 5: 1}
--------------------------------------------------
dict.num_nnz = 8
--------------------------------------------------
dict.num_docs = 3
--------------------------------------------------
dict.num_pos = 10
--------------------------------------------------
dict.doc2bow(docs[0]) = [(0, 1), (1, 2), (2, 1)]
--------------------------------------------------
dict.doc2idx(docs[0]) = [0, 1, 2, 1]
--------------------------------------------------
~~~

#### BOW（Bag of Word）

通过统计文档的BOW来，重新构建语料库。

~~~python
print(dictionary.token2id)

bow_corpus = [dictionary.doc2bow(text) for text in processed_corpus]
pprint(bow_corpus)
~~~

![image-20200609093123150](images/image-20200609093123150.png)

每篇文档由一个向量表示，由于文本的稀疏性，仅仅记录哪些数量大于零的word。

### 模型（Model）

模型可以看成是一种转换（transformation），即把语料库的向量空间（vector space）转化为模型所在的向量空间。比如：  [tf-idf](https://en.wikipedia.org/wiki/Tf–idf)。它根据word在语料库中的稀缺性对BOW进行加权。

~~~python
from gensim import models

# train the model
tfidf = models.TfidfModel(bow_corpus)

# transform the "system minors" string
words = "system minors".lower().split()
doc = dictionary.doc2bow(words)
print(dod)
print(tfidf[doc])
~~~

![image-20200609094514104](images/image-20200609094514104.png)

> The tf-idf model transforms vectors from the bag-of-words representation to a vector space where the frequency counts are weighted according to the relative rarity of each word in the corpus.

进一步可以获得基于tf-idf的语料库。

~~~python
tfidf_corpus =  tfidf[bow_corpus]
print('-'*50)
pprint(bow_corpus)
print('-'*50)
pprint([[(id, round(tfidf, 4))for id, tfidf in doc] for doc in tfidf_corpus])
~~~

![image-20200609095802255](images/image-20200609095802255.png)

除了tf-idf模型，gensim还支持很多其它模型，比如：LSI（[Latent Semantic Indexing](https://en.wikipedia.org/wiki/Latent_semantic_indexing)），RP（[Random Projections](http://www.cis.hut.fi/ella/publications/randproj_kdd.pdf)）, LDA（[Latent Dirichlet Allocation](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation)），HDP（[Hierarchical Dirichlet Process](http://jmlr.csail.mit.edu/proceedings/papers/v15/wang11a/wang11a.pdf)）。

接下来，我们就可以进行相似性比较了。比如，下面使用[SparseMatrixSimilarity](https://tedboy.github.io/nlps/generated/generated/gensim.similarities.SparseMatrixSimilarity.html)，它采用cosine similarity来计算向量之间的相似性。

~~~python
from gensim import similarities

index = similarities.SparseMatrixSimilarity(tfidf_corpus, num_features=12)

query_document = 'system engineering'.split()
query_bow = dictionary.doc2bow(query_document)
sims = index[tfidf[query_bow]]

# 排序
for document_number, score in sorted(enumerate(sims), key=lambda x: x[1], reverse=True):
    print((document_number, text_corpus[document_number], score))
~~~

![image-20200609105339068](images/image-20200609105339068.png)

除了[SparseMatrixSimilarity](https://tedboy.github.io/nlps/generated/generated/gensim.similarities.SparseMatrixSimilarity.html)，gensim还包含其它相似性计算的类，比如：[MatrixSimilarity](https://radimrehurek.com/gensim/similarities/docsim.html#gensim.similarities.docsim.MatrixSimilarity)，[WmdSimilarity](https://radimrehurek.com/gensim/similarities/docsim.html#gensim.similarities.docsim.WmdSimilarity)。

### Corpus Streaming

上面的例子中，语料库被完整的加载到内存中，然后，实际工作中，语料库往往包含几百万甚至更多的文档，没有办法能够一次加载到内存中来，所以必须要采用Streaming的方式来读取数据。下面是一个例子。

~~~shell
cat << EOF > data/mycorpus.txt
Human machine interface for lab abc computer applications
A survey of user opinion of computer system response time
The EPS user interface management system
System and human system engineering testing of EPS
Relation of user perceived response time to error measurement
The generation of random binary unordered trees
The intersection graph of paths in trees
Graph minors IV Widths of trees and well quasi ordering
Graph minors A survey
EOF

~~~























## 参考

