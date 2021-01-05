---
# generated from _notes/05-ai/54-tensorflow/keras_text_data.md

title: Keras文本数据集
categories: others
date: 2021-01-05
---

keras.datasets中内置了一些数据集，这些数据往往作为benchmark，非常的常用。本文将讲解其中两个文本数据集的使用方法。

- imdb：数据集来自 IMDB 的电影评论，以情绪（正面/负面）标记。其中训练集和测试集的都是 25,000 条评论。所有评论已经过预处理，并编码为词索引（整数）的序列表示。
- reuters：数据集来源于路透社的 11,228 条新闻文本（包含训练数据和测试数据），总共分为 46 个主题。与 IMDB 数据集一样，每条新闻都被编码为一个词索引的序列（相同的约定）。

由于这两个数据集使用方法几乎完全相同，下面以reuters数据集为例，讲解其中用法。reuters有两个方法。

- load_data：加载数据。
- get_word_index：返回一个word->index的字典。

## 实例

下面来实际调用一下。可以看到数据集被分成了训练和测试两部分。

~~~python
from tensorflow.keras import datasets

(x_train, y_train), (x_test, y_test) = datasets.reuters.load_data()

print(x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)
~~~

![image-20210105122910102](/assets/images/image-20210105122910102.png)

然后看看里面的数据。

~~~python
classes = ['cocoa','grain','veg-oil','earn','acq','wheat','copper','housing','money-supply',
   'coffee','sugar','trade','reserves','ship','cotton','carcass','crude','nat-gas',
   'cpi','money-fx','interest','gnp','meal-feed','a[','iron-steel','rubber','heat','jobs',
   'lei','bop','zinc','orange','pet-chem','dlr','gas','silver','wpi','hog','lead']

np.random.seed(1031)
samples = np.random.randint(0, 100, 3)
for i in samples:
    title = "Sample {}: {} {}, {} words".format(i, y_train[i], classes[y_train[i]], len(x_train[i]))
    print('-'*40, title,'-'*40)
    print(x_train[i]) 
~~~

![image-20210105134539974](/assets/images/image-20210105134539974.png)

可以看到里面的每一条新闻保存的并不是实际的文本，而是文本后面所代表的编号，要获得实际的文本，还需要通过`get_word_index`方法得到词典表，然后根据词典转换才行。下面看看词典。

~~~python
word_index = datasets.reuters.get_word_index()
index_word = {value:key for key,value in word_index.items()}

[(index_word[i],i) for i in range(1, 11)]
~~~

![image-20210105125557319](/assets/images/image-20210105125557319.png)

上面代码显示频次最高的10个词，这些词往往高频，但没有特别的意义。下面通过词典表转换，看看实际的文本。

~~~python
for i in samples:
    title = "Sample {}: {} {}, {} words".format(i, y_train[i], classes[y_train[i]], len(x_train[i]))
    print('-'*40, title,'-'*40)
    print(' '.join([index_word[i]  for i in x_train[i] if i>index_from]))
~~~

![image-20210105134619754](/assets/images/image-20210105134619754.png)

上面的文本，好像都完全没法看到，这是因为word_index中按照词频排序，起始的编号是1，而load_data方法默认参数index_from是3（下节有详细说明），表示词典起始编号是大于3的。由此，我们需要对词典表的需要做一些调整。

~~~python
index_from = 3
word_index = datasets.reuters.get_word_index()
word_index = {key:value+index_from for key,value in word_index.items()}
index_word = {value:key for key,value in word_index.items()}

[(index_word[i],i) for i in range(1+index_from, 11+index_from)]
~~~

![image-20210105130657006](/assets/images/image-20210105130657006.png)

可以看到词频最高的词the，它的编号是4。然后再来转换一下，看看实际的文本。

~~~python
for i in samples:
    title = "Sample {}: {} {}, {} words".format(i, y_train[i], classes[y_train[i]], len(x_train[i]))
    print('-'*40, title,'-'*40)
    print(' '.join([index_word[i]  for i in x_train[i] if i>index_from]))
~~~

![image-20210105134707122](/assets/images/image-20210105134707122.png)

## 详细说明

~~~python
def get_word_index(path='reuters_word_index.json')
    
def load_data(path='reuters.npz',
              num_words=None, 
              skip_top=0,
              maxlen=None,
              test_split=0.2,
              seed=113,
              start_char=1,
              oov_char=2,
              index_from=3,
              **kwargs):
~~~

get_word_index参数比较简单，下面详细说明load_data方法的参数。

- path：数据保存的文件路径。默认值是reuters.npz，文件将保存在`~/.keras/datasets/reuters.npz`。
- num_words ：词的个数。由于所有的词的index都是按照词频大小排列的，所以如果num_words 指定100，则index大于等于100的词都会被忽略。默认为None，表示不会忽略任何词。
- skip_top ：要忽略的热门（但无意义）的词汇（比如：the，of，to等）。默认为None，表示不会忽略任何词。
- maxlen：序列最大长度，如果超过maxlen的序列，会进行截断。默认为None，表示不限制长度。
- seed：随机种子
- start_char：序列开始的标记。默认为1，故在上文示例数据中，每条新闻的第一个词编号都是1。如果设置成None，则不会添加开始标记。
- oov_char：（由于num_words或者skip_top的限制）被去掉的词用这个字符代替。默认为2.
- index_from：词的起始编号大于该值。

下面的例子中，设置了num_words=100, skip_top=10。

~~~python
(x_train, y_train), (x_test, y_test) = datasets.reuters.load_data(num_words=100, skip_top=10)
print(x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)
~~~

可以看到top 10的高频词被移除了，同时top 100之后的词也被忽略了。所有这些词都会被2（oov_char=2）替代。

~~~python
(x_train, y_train), (x_test, y_test) = datasets.reuters.load_data(num_words=100)
all_words = np.unique(np.array([w for sent in np.concatenate((x_train, x_test)) for w in sent]))

all_words.sort()
print(all_words[0:10])
print(all_words[-10:])
~~~

![image-20210105135038489](/assets/images/image-20210105135038489.png)

最后看看具体的数据，由于发现num_words设置的很小，所以好多文本都被替换成了2。

~~~python
for i in samples:
    title = "Sample {}: {} {}, {} words".format(i, y_train[i], classes[y_train[i]], len(x_train[i]))
    print('-'*40, title,'-'*40)
    print(x_train[i]) 
~~~

![image-20210105135131206](/assets/images/image-20210105135131206.png)

## 参考

- [常用数据集 Datasets](https://keras.io/zh/datasets)

- [keras中7大数据集datasets介绍](https://blog.csdn.net/weixin_41770169/article/details/80249986)

  
