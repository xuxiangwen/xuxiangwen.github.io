## Table of Contents

### Week 1

#### Week_1_device_placement.ipynb

TF运行的设备，可以GPU或CPU。比较了CPU和GPU在矩阵加法，矩阵乘法，模型训练上的性能差异，对于相同任务，情况如下。

#### Week_1_functional_api.ipynb 

详细描述了TF Functional API，具体内容如下：

- 多个input和output的模型
- Tensors and Variables
- 访问模型中的layer：主要用transfer learning的例子来说明。
- Freezing layers：设置模型的某些layer，训练时不会更新参数。

#### Week_1_Layer_nodes.ipynb

介绍了多个input和output的模型需要注意的东西。

> 目前看起来好像没啥用，但或许要用到，才能体会。

#### Week_1_Programming_Assignment.ipynb 

第一周的大作业。主要使用Transfer learning来训练[Dogs vs Cats dataset](https://www.kaggle.com/c/dogs-vs-cats/data)。

### Week 2

#### Week_2_Creating_Datasets_from_different_sources.ipynb

- 介绍了`from_tensor_slices` and `from_tensors`之前的区别。看起来from_tensors好像很少会用到。
  - 从numpy的narray中创建Dataset
  - 从pandas的DataFrame中创建Dataset
- 导入csv文件创建Dataset

#### Week_2_Data_Pipeline.ipynb 

-  介绍keras的dataset。也就是大多教程例子在用的方式。
  - 加载CIFAR-100数据集。介绍了一些不同参数的作用
  - 加载IMDB数据集。介绍了一些不同参数的作用，尤其对于文本处理比较有用。
- 介绍Dataset Generator。这种方式主要使用yield来实现数据的加载。
  和keras的dataset相比，可以自定义数据的获取方式，同时可以不用一次把所有数据加到内存中去。
- 介绍了keras的data augmentation
- 介绍了Dataset Class：这个实际时TF的亲生儿子。
- 使用Dataset  Class，进行数据预处理，和模型训练。总体感觉有些功能很啰嗦复杂，实际中未必会用到那么多。

#### Week_2_Keras_TimeseriesGenerator.ipynb 

使用时间序列处理TimeseriesGenerator处理音频的例子，挺不错。

#### Week_2_Programming_Assignment.ipynb

第二周的大作业。主要两部分：

- 对于一个The LSUN Dataset很小的子集，采用data augmentation减少数据过拟合
- 对于CIFAR-100数据集，创建Dataset，添加filter，使用map对数据进行一些修改。

#### Week_2_TensorFlow_Datasets.ipynb

使用tensorflow-datasets来加载数据集，和keras的dataset，总计感觉要麻烦一些。但这时TF的亲儿子，从设计上应该能够满足更多的需求。

