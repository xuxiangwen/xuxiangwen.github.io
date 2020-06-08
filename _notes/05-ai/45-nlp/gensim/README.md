



### gensim.corpora.dictionary.Dictionary

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

