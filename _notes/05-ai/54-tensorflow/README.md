

### [Keras中文文档](https://keras.io/zh/)

由于tensorflow2.0采用了keras的API，看这里更加的清晰。

### [Colab](https://colab.research.google.com/)

Colaboratory（简称Colab）是一个免费的 Jupyter 笔记本环境，不需要进行任何设置就可以使用，并且完全在云端运行。借助 Colab，您可以编写和执行代码、保存和共享分析结果，以及利用强大的计算资源，所有这些都可通过浏览器免费使用。

在Colab中，可以code和text之间切换。

- code to text： Ctrl + m + m
- text to code: Ctrl + m + y

### [AI Hub](https://aihub.cloud.google.com/)

Google正在推出两种新工具，一种是专有工具，另一种是开放源代码：AI Hub和Kubeflow管道。两者均旨在协助数据科学家设计，启动和跟踪其机器学习算法。

借助AI Hub和Kubeflow管道，Google 将于 1月份发布其较早版本的Cloud AutoML，并继续其简化和加快客户适应Google AI技术和服务的能力的战略。Cloud ML Platform的工程总监Hussein Mehanna在博客中写道：

我们的目标是使AI覆盖所有业务。但这意味着降低准入门槛。这就是为什么我们在构建所有AI产品时会牢记三个想法的原因：简化它们，使更多的企业可以采用它们，使它们对最广泛的组织有用，并使其快速发展，以便企业可以迭代并更快地获得成功。

Google引入了AI Hub，使AI可以更广泛地接触企业，使他们更容易发现，共享和重用现有工具和工作。此外，AI Hub是ML内容的一站式目的地，例如管道，Jupyter笔记本和TensorFlow模块。根据Mehanna所说的好处是：

由Google Cloud AI，Google Research和其他Google团队开发的高质量ML资源对所有企业都是公开可用的。

> 好像就是之前说的seedbank。

### TensorFlow API Document

https://www.tensorflow.org/api_docs/python/tf

### [Keras Applictions](https://keras.io/api/applications/)

Kera的应用模块Application提供了带有预训练权重的Keras模型，这些模型可以用来进行预测、特征提取和finetune

### [Tensorflow Hub](https://www.tensorflow.org/hub)

TensorFlow Hub 是一个包含经过训练的机器学习模型的代码库，这些模型稍作调整便可部署到任何设备上。您只需几行代码即可重复使用经过训练的模型，例如 BERT 和 Faster R-CNN。

## Scratch

### tf.clip_by_value

~~~python
import tensorflow as tf;
import numpy as np;
 
A = np.array([[1,1,2,4], [3,4,8,5]])
tf.clip_by_value(A, 2, 5)
~~~

![image-20201216160335336](images/image-20201216160335336.png)

### Tokenizer

- https://keras-cn.readthedocs.io/en/latest/preprocessing/text/
- http://codewithzhangyi.com/2019/04/23/keras-tokenizer/

#### 构造器参数

- **num_words**: 默认是`None`处理所有字词，但是如果设置成一个整数，那么最后返回的是最常见的、出现频率最高的`num_words`个字词。一共保留 `num_words-1` 个词。
- **filters**: 过滤一些特殊字符，默认上文的写法就可以了。
- **lower**: 是否全部转为小写。
- **split**: 分词的分隔符字符串，默认为空格。因为英文分词分隔符就是空格。
- **char_level**: 分字。
- **oov_token**: if given, it will be added to word_index and used to replace out-of-vocabulary words during text_to_sequence calls

#### 方法

| 方法                                | 参数                                                         | 返回值                                                       |
| :---------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| fit_on_texts(texts)                 | texts：要用以训练的文本列表                                  | -                                                            |
| texts_to_sequences(texts)           | texts：待转为序列的文本列表                                  | 序列的列表，列表中每个序列对应于一段输入文本                 |
| texts_to_sequences_generator(texts) | texts：待转为序列的文本列表                                  | 本函数是texts_to_sequences的生成器函数版，返回每次调用返回对应于一段输入文本的序列 |
| texts_to_matrix(texts, mode)        | texts：待向量化的文本列表；mode：‘binary’，‘count’，‘tfidf’， ‘freq’之一，默认为‘binary’ | 形如(len(texts), nb_words)的numpy array                      |
| fit_on_sequences(sequences)         | sequences：要用以训练的序列列表                              | -                                                            |
| sequences_to_matrix(sequences)      | sequences：待向量化的序列列表； mode：同上                   | 返回值：形如(len(sequences), nb_words)的numpy array          |

代码示例：

~~~python
from tensorflow.keras.preprocessing.text import Tokenizer

sentences = [
    'i love my dog, i',
    'I, love my cat',
    'You love my dog!'
]

tokenizer = Tokenizer(num_words = 100)
tokenizer.fit_on_texts(sentences)

print('-'*25, '设置', '-'*25)
print('char_level= ', tokenizer.char_level)         # 是否是字符级别
print('lower= ', tokenizer.lower)                   # 大小写
print('oov_token= ', tokenizer.oov_token)           # out of vocabulary的token			
print('num_words= ', tokenizer.num_words)           # 最大word个数

print('-'*25, '具体信息', '-'*25)
print('document_count =', tokenizer.document_count) # 文档数量
print('word_index= ', tokenizer.word_index)         # word:index字典
print('index_word= ', tokenizer.index_word)         # index:word字典
print('word_docs= ', tokenizer.word_docs)           # word在文档出现的次数（同一文档出现多次算一次）
print('index_docs= ', tokenizer.index_docs)         # 同上，只是key是index
print('word_counts= ', tokenizer.word_counts)       # word出现的次数

~~~

![image-20201219203748006](images/image-20201219203748006.png)