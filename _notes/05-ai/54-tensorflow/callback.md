---
title: Callback
categories: deep-learning
date: 2020-11-09
---

本文将介绍Tensorflow中的Callback。它是一个非常有用的工具，用于自定义train，evaluate和predict中的行为。

## Callback的方法

实现Callback很简单，主要有两步：

- 创建一个新的类，这个类继承`tf.keras.callbacks.Callback`。

- 根据需求，重载tf.keras.callbacks.Callback`中的如下方法。
  - `on_(train|test|predict)_begin(self, logs=None)`
  - `on_(train|test|predict)_end(self, logs=None)`
  - `on_(train|test|predict)_batch_begin(self, batch, logs=None)`
  - `on_(train|test|predict)_batch_end(self, batch, logs=None)`
  - `on_epoch_begin(self, epoch, logs=None)`
  - `on_epoch_end(self, epoch, logs=None)`

  以上所有`begin`结尾方法，其logs是一个空的list。而end结尾的方法，其logs大多是有内容的，详见后文。

完成了前两步准备后，在模型训练，评估或预测时，把Callback类传入，则上面的那些方法将会被调用。其调用的具体的规则如下。

- `tf.keras.Model.fit()`

  Callback中方法调用顺序的伪代码如下。

  ~~~python
  on_train_begin(self, logs=None)
  for epoch in epoches:
  	on_epoch_begin(self, epoch, logs=None)
      for batch in train_batches:
          on_train_batch_begin(self, batch, logs=None)
          on_train_batch_end(self, batch, logs=None) 	# logs.keys = [loss, ...]        
      on_test_begin(self, logs=None)
      for batch in test_batches:
          on_test_batch_begin(self, batch, logs=None)
          on_test_batch_end(self, batch, logs=None)： # logs.keys = [loss, ...]
      on_test_end(self, logs=None)					# logs.keys = [loss, ...]    
      on_epoch_end(self, epoch, logs=None)			# logs.keys = [loss, val_loss, ...]
  on_train_end(self, logs=None)						# logs.keys = [loss, val_loss, ...]
  ~~~

- `tf.keras.Model.evaluate()`

  Callback中方法调用顺序的伪代码如下。

  ~~~python
  on_test_begin(self, logs=None)
  for batch in test_batches:
  	on_test_batch_begin(self, batch, logs=None)			
      on_test_batch_end(self, batch, logs=None)   	# logs.keys = [loss, ...] 
  on_test_end(self, logs=None)						# logs.keys = [loss, val_loss, ...]
  ~~~

- `tf.keras.Model.predict()`

  Callback中方法调用顺序的伪代码如下。

  ~~~python
  on_predict_begin(self, logs=None)
  for batch in test_batches:
  	on_predict_batch_begin(self, batch, logs=None)	
  	on_predict_batch_end(self, batch, logs=None)	# logs = [outputs, ...] 
  on_predict_end(self, logs=None)
  ~~~

## Callback实践

### 调用顺序

下面的代码展示了Callback中方法的调用顺序。首先创建模型和加载数据。

~~~python
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow import keras

gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
tf.config.experimental.set_virtual_device_configuration(
    gpus[0],
    [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024)]
)

def get_model():
    model = keras.models.Sequential()
    model.add(keras.layers.Flatten(input_shape=(28, 28)))
    model.add(keras.layers.Dense(128, activation='relu'))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(10))    
    model.compile(
        optimizer=keras.optimizers.RMSprop(learning_rate=0.1),
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )
    return model

def get_mnist():
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0
    return x_train, y_train, x_test, y_test

~~~

然后自定义Callback类。

~~~python
class CustomCallback(keras.callbacks.Callback):
    def on_train_begin(self, logs=None):
        keys = list(logs.keys())
        print("Starting training; got log keys: {}".format(keys))

    def on_train_end(self, logs=None):
        keys = list(logs.keys())
        print("Stop training; got log keys: {}".format(keys))

    def on_epoch_begin(self, epoch, logs=None):
        keys = list(logs.keys())
        print("Start epoch {} of training; got log keys: {}".format(epoch, keys))

    def on_epoch_end(self, epoch, logs=None):
        keys = list(logs.keys())
        print("End epoch {} of training; got log keys: {}".format(epoch, keys))

    def on_test_begin(self, logs=None):
        keys = list(logs.keys())
        print("Start testing; got log keys: {}".format(keys))

    def on_test_end(self, logs=None):
        keys = list(logs.keys())
        print("Stop testing; got log keys: {}".format(keys))

    def on_predict_begin(self, logs=None):
        keys = list(logs.keys())
        print("Start predicting; got log keys: {}".format(keys))

    def on_predict_end(self, logs=None):
        keys = list(logs.keys())
        print("Stop predicting; got log keys: {}".format(keys))

    def on_train_batch_begin(self, batch, logs=None):
        keys = list(logs.keys())
        print("    Training: start of batch {}; got log keys: {}".format(batch, keys))

    def on_train_batch_end(self, batch, logs=None):
        keys = list(logs.keys())
        print("    Training: end of batch {}; got log keys: {}".format(batch, keys))

    def on_test_batch_begin(self, batch, logs=None):
        keys = list(logs.keys())
        print("    Evaluating: start of batch {}; got log keys: {}".format(batch, keys))

    def on_test_batch_end(self, batch, logs=None):
        keys = list(logs.keys())
        print("    Evaluating: end of batch {}; got log keys: {}".format(batch, keys))

    def on_predict_batch_begin(self, batch, logs=None):
        keys = list(logs.keys())
        print("    Predicting: start of batch {}; got log keys: {}".format(batch, keys))

    def on_predict_batch_end(self, batch, logs=None):
        keys = list(logs.keys())
        print("    Predicting: end of batch {}; got log keys: {}".format(batch, keys))

~~~

下面来进行模型训练，评估和预测。

~~~python
x_train, y_train, x_test, y_test = get_mnist()
x_train = x_train[:1024]
y_train = y_train[:1024]
x_test = x_test[:512]
y_test = y_test[:512]

model = get_model()
model.fit(
    x_train,
    y_train,
    batch_size=256,
    epochs=1,
    verbose=0,
    validation_split=0.5,
    callbacks=[CustomCallback()],
)

print('-'*100)
res = model.evaluate(
    x_test, y_test, batch_size=256, verbose=0, callbacks=[CustomCallback()]
)

print('-'*100)
res = model.predict(x_test, batch_size=256, callbacks=[CustomCallback()])
~~~

![image-20201108175730619](images/image-20201108175730619.png)

### Early Stopping

在模型训练时，为了减少过拟合，往往会采用Early Stopping的技术。它会比较某一个metrics（最常用的是`val_loss`）是否在持续在降低，如果连续几个epochs都没有降低，将会中止训练，而且往往会把参数恢复到之前metrics最低时候的参数。

下面自定义的类实现了Early Stopping的逻辑。下面代码中，当设置`self.model.stop_training = True`后，训练将会退出。

~~~python
class MyEarlyStopping(keras.callbacks.Callback):
    """Stop training when the loss is at its min, i.e. the loss stops decreasing.

  Arguments:
      patience: Number of epochs to wait after min has been hit. After this
      number of no improvement, training stops.
  """

    def __init__(self, patience=0):
        super(MyEarlyStopping, self).__init__()
        self.patience = patience
        self.best_weights = None
        self.best_epoch = -1

    def on_train_begin(self, logs=None):
        self.wait = 0
        self.stopped_epoch = 0
        self.best = np.Inf

    def on_epoch_end(self, epoch, logs=None):
        current = logs.get("val_loss")
        if np.less(current, self.best):
            self.best = current
            self.best_epoch = epoch
            self.wait = 0
            self.best_weights = self.model.get_weights()
        else:
            self.wait += 1
            if self.wait >= self.patience:
                self.stopped_epoch = epoch
                self.model.stop_training = True
                print("Restoring model weights from the end of the best epoch {}.".format(self.best_epoch+1))
                self.model.set_weights(self.best_weights)

    def on_train_end(self, logs=None):
        if self.stopped_epoch > 0:
            print("Epoch %05d: early stopping" % (self.stopped_epoch + 1))
            
model = get_model()
history = model.fit(
    x_train,
    y_train,
    batch_size=256,
    epochs=30,
    verbose=0,
    validation_split=0.5,
    callbacks=[MyEarlyStopping(patience=5)],    
)
~~~

![image-20201109022827577](images/image-20201109022827577.png)

下面来显示训练过程中的val_loss趋势。

~~~python
def plot_history(history, metrics_name='accuracy'):
    plt.figure(figsize=(8, 4))
    # 忽略前面几个epoch
    start_epoch = 5    
    metrics = history.history[metrics_name][start_epoch-1:]
    val_metrics = history.history['val_' + metrics_name][start_epoch-1:]
    epochs = [start_epoch + i for i in range(len(metrics))]
    lowest = np.argmin(val_metrics)
    
    plt.plot(epochs, metrics, label=metrics_name)
    plt.plot(epochs, val_metrics, label = 'val_' + metrics_name)
    plt.plot(lowest+start_epoch, val_metrics[lowest], 'ro')
    plt.xlabel('epoch')
    plt.ylabel(metrics_name)
    plt.xticks(epochs)
    plt.legend(loc='upper right')
    plt.show()

plot_history(history, metrics_name='loss')
~~~

![image-20201109023043836](images/image-20201109023043836.png)

上图中第15 epoch，val_loss获得最低的值，接下来五轮epoch，val_loss无法获得更低的值，所以训练退出。

TensorFlow在tf.keras.callbacks.EarlyStopping类中也实现的Early Stopping功能，其逻辑和上面的实现基本相同。

```py
tf.keras.callbacks.EarlyStopping(
    monitor='val_loss', 
    min_delta=0, 
    patience=0, 
    verbose=0, 
    mode='auto',
    baseline=None, 
    restore_best_weights=False
)
```

如果调用`keras.callbacks.EarlyStopping`，效果完全一样。

~~~python
model = get_model()
history = model.fit(
    x_train,
    y_train,
    batch_size=256,
    epochs=30,
    verbose=0,
    validation_split=0.5,
    callbacks=[keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)],    
)
plot_history(history, metrics_name='loss')
~~~

![image-20201109024441079](images/image-20201109024441079.png)

## 参考

- [Writing your own callbacks](https://www.tensorflow.org/guide/keras/custom_callback)
