本课程来自Coursera上的课程[Getting started with TensorFlow 2](https://www.coursera.org/learn/getting-started-with-tensor-flow2/home/welcome)，是系列课程[TensorFlow 2 for Deep Learning Specialization](https://www.coursera.org/specializations/tensorflow2-deeplearning)的第一个课程。

### Week 1：Introduction to TensorFlow

介绍了一下tensorflow和相关资源。

### Week 2：The Sequential model API

#### [The Sequential model API](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/getting-started-with-tensor-flow2/Week_2_The%20Sequential%20model%20API.ipynb)

使用Sequential model的卷积神经网络入门示例。数据集为fashion_mnist。

#### [Week 2 Programming Assignment](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/getting-started-with-tensor-flow2/Week_2_Programming_Assignment.ipynb)

和上面的文档非常相似，也是使用Sequential model的卷积神经网络入门示例。数据集为[MNIST dataset](http://yann.lecun.com/exdb/mnist/)。

### Week 3：Validation, regularisation and callbacks

#### [Additional callbacks](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/getting-started-with-tensor-flow2/Week_3_Additional_callbacks.ipynb)

介绍了另外几种Callback:

- LearningRateScheduler
- CSVLogger
- Lambda callbacks
- ReduceLROnPlateau

#### [Validation, regularisation and callbacks](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/getting-started-with-tensor-flow2/Week_3_validation_regularisation_callbacks.ipynb)

介绍了Validation数据集，正则化（Regularisation）和Callback

- 正则化（Regularisation）
  - BatchNormalization
  - Dropout
  - kernel_regularizer
- Callback
  - EarlyStopping

#### [Week_3_Programming_Assignment](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/getting-started-with-tensor-flow2/Week_3_Programming_Assignment.ipynb)

对 [Iris dataset](https://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html)数据集进行分类。采用正则化和EarlyStopping减少过拟合。

### Week 4：Saving and loading models

#### [Saving model architecture only](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/getting-started-with-tensor-flow2/Week_4_Saving_model_architecture_only.ipynb)

不保存weights，仅仅保存模型的architecture。可以保存的方式有：config， JSON 和YAML

#### [Saving and loading models](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/getting-started-with-tensor-flow2/Week_4_Saving_and_loading_models.ipynb)

介绍了多种模型保存加载的方式。尤其是:

- Load pre-trained Keras models

  ~~~python
  from tensorflow.keras.applications import ResNet50
  model = ResNet50(weights='imagenet')
  ~~~

- Load Tensorflow Hub modules

  ~~~python
  import tensorflow_hub as hub
  module_url = "https://tfhub.dev/google/imagenet/mobilenet_v1_050_160/classification/4"
  model = Sequential([hub.KerasLayer(module_url)])
  model.build(input_shape=[None, 160, 160, 3])
  ~~~

#### [Week 4 Programming Assignment](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/getting-started-with-tensor-flow2/Week_4_Programming_Assignment.ipynb)

对 [EuroSAT dataset](https://github.com/phelber/EuroSAT)数据集进行分类。使用ModelCheckpoint来保存模型。

~~~python
 # 加载最后的模型
 model.load_weights(tf.train.latest_checkpoint('checkpoints_every_epoch'))
 # 加载最佳的模型
 model.load_weights('./checkpoints_best_only/checkpoint')
~~~

### Week 5: Capstone Project

对[SVHN dataset](http://ufldl.stanford.edu/housenumbers/)数据集进行分类，运用本课程所学技术，创建了MLP和CNN模型。

- 使用ModelCheckpoint保存最佳模型
- 使用EarlyStopping，避免模型过度拟合
- 运用BatchNormalization和Dropout来减少过拟合

Below is my submit. 

https://www.coursera.org/learn/getting-started-with-tensor-flow2/peer/7toR2/capstone-project/submit

下面是论坛里的求大家review的帖子：

https://www.coursera.org/learn/getting-started-with-tensor-flow2/discussions/weeks/5/threads/JEMe1IeUEeuIoBJBxR0Gqw