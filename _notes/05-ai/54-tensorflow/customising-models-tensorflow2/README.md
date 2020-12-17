## Table of Contents

### Week 1

#### [Week_1_functional_api.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/customising-models-tensorflow2/Week_1_functional_api.ipynb)

TF运行的设备，可以GPU或CPU。比较了CPU和GPU在矩阵加法，矩阵乘法，模型训练上的性能差异，对于相同任务，情况如下。

#### [Week_1_functional_api.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/customising-models-tensorflow2/Week_1_functional_api.ipynb)

详细描述了TF Functional API，具体内容如下：

- 多个input和output的模型
- Tensors and Variables
- 访问模型中的layer：主要用transfer learning的例子来说明。
- Freezing layers：设置模型的某些layer，训练时不会更新参数。

#### [Week_1_Layer_nodes.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/customising-models-tensorflow2/Week_1_Layer_nodes.ipynb)

介绍了多个input和output的模型需要注意的东西。

> 目前看起来好像没啥用，但或许要用到，才能体会。

#### [Week_1_Programming_Assignment.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/customising-models-tensorflow2/Week_1_Programming_Assignment.ipynb)

第一周的大作业。主要使用Transfer learning来训练[Dogs vs Cats dataset](https://www.kaggle.com/c/dogs-vs-cats/data)。

### Week 2

#### [Week_2_Creating_Datasets.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/customising-models-tensorflow2/Week_2_Creating_Datasets.ipynb)

从不同数据源创建Dataset。

- 介绍了`from_tensor_slices` and `from_tensors`之前的区别。看起来from_tensors好像很少会用到。
  - 从numpy的narray中创建Dataset
  - 从pandas的DataFrame中创建Dataset
- 导入csv文件创建Dataset

#### [Week_2_Data_Pipeline.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/customising-models-tensorflow2/Week_2_Data_Pipeline.ipynb)

-  介绍keras的dataset。也就是大多教程例子在用的方式。
  - 加载CIFAR-100数据集。介绍了一些不同参数的作用
  - 加载IMDB数据集。介绍了一些不同参数的作用，尤其对于文本处理比较有用。
- 介绍Dataset Generator。这种方式主要使用yield来实现数据的加载。
  和keras的dataset相比，可以自定义数据的获取方式，同时可以不用一次把所有数据加到内存中去。
- 介绍了keras的data augmentation
- 介绍了Dataset Class：这个实际时TF的亲生儿子。
- 使用Dataset  Class，进行数据预处理，和模型训练。总体感觉有些功能很啰嗦复杂，实际中未必会用到那么多。

#### [Week_2_Keras_TimeseriesGenerator.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/customising-models-tensorflow2/Week_2_Keras_TimeseriesGenerator.ipynb)

使用时间序列处理TimeseriesGenerator处理音频的例子，挺不错。

#### [Week_2_Programming_Assignment.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/customising-models-tensorflow2/Week_2_Programming_Assignment.ipynb)

第二周的大作业。主要两部分：

- 对于一个The LSUN Dataset很小的子集，采用data augmentation减少数据过拟合
- 对于CIFAR-100数据集，创建Dataset，添加filter，使用map对数据进行一些修改。

#### [Week_2_TensorFlow_Datasets.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/customising-models-tensorflow2/Week_2_TensorFlow_Datasets.ipynb)

使用tensorflow-datasets来加载数据集，和keras的dataset，总计感觉要麻烦一些。但这时TF的亲儿子，从设计上应该能够满足更多的需求。

### Week 3

#### [Week_3_Programming_Assignment.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/customising-models-tensorflow2/Week_3_Programming_Assignment.ipynb)

使用Shakespeare dataset训练character-level 语言模型，能够自动的生成文本。主要使用了Tokenizer来进行文本预处理，然后创建模型，使用Stateful方式在batch之间来保持Hide State。模型训练的速度真的很慢，看来必须要使用Attention等技术，一般可以并行处理，提高速度。

为了batch之间共享State福利，准备数据的处理技巧如下：

~~~python
num_processed_examples = 50
steps = 5
inx = np.empty((0,), dtype=np.int32)
for i in range(steps):
    inx = np.concatenate((inx, i + np.arange(0, num_processed_examples, steps)))

print(inx)
print(len(inx), inx.shape)
~~~

![image-20201216093735021](images/image-20201216093735021.png)

上面这样处理的目的是，当一个batch训练完成后，下一个batch也能共享上次得隐藏状态。这样如下文所示，连续五个句子（比如：0，1，2，3，4）可以共享隐藏状态。
~~~
0  5 10 15 20 25 30 35 40 45  
1  6 11 16 21 26 31 36 41 46  
2  7 12 17 22 27 32 37 42 47  
3  8 13 18 23 28 33 38 43 48  
4  9 14 19 24 29 34 39 44 49  
~~~

#### [Week_3_Sequence_modelling.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/customising-models-tensorflow2/Week_3_Sequence_modelling.ipynb)

介绍了Sequence模型中的多个处理技术和多个层次

- Padding
- Embedding Layer
- Embedding Projector：可以把Embedding Layer生成的词向量导入到网站[projector.tensorflow.org](https://projector.tensorflow.org/)，可视化展现其关系。
- RNN
  - SimpleRNN, LSTM, GRU
  - Stacked RNNs and the Bidirectional wrapper

#### [Week_3_Stateful_RNNs.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/customising-models-tensorflow2/Week_3_Stateful_RNNs.ipynb)

介绍了Stateful RNN的使用。

- Bidirectional里面只有backward_layer的States有内容，而layer得States是None，原因何在？

  ~~~python
  inputs = Input(batch_shape=(2, None, 1))
  outputs = Bidirectional(layer=LSTM(5, stateful=True, name='stateful_rnn'))(inputs)
  # outputs = Bidirectional(layer=LSTM(5, stateful=True, name='stateful_rnn'),
  #                         backward_layer = GRU(5, stateful=True, name='backward_stateful_rnn', go_backwards=True)
  #                        )(inputs)
  
  stateful_gru = Model(inputs=inputs, outputs=outputs)
  stateful_gru.summary()
  ~~~

  ![image-20201216092618086](images/image-20201216092618086.png)

#### [Week_3_Tokenising_Text_Data.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/customising-models-tensorflow2/Week_3_Tokenising_Text_Data.ipynb)

使用Tokenizer来处理文本。里面添加了很多相关的属性和方法的描述，

