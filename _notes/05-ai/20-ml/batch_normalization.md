## tf.layers.batch_normalization()方法

方法接口如下：

```python
tf.layers.batch_normalization(
    inputs,
    axis=-1,
    momentum=0.99,
    epsilon=0.001,
    center=True,
    scale=True,
    beta_initializer=tf.zeros_initializer(),
    gamma_initializer=tf.ones_initializer(),
    moving_mean_initializer=tf.zeros_initializer(),
    moving_variance_initializer=tf.ones_initializer(),
    beta_regularizer=None,
    gamma_regularizer=None,
    beta_constraint=None,
    gamma_constraint=None,
    training=False,
    trainable=True,
    name=None,
    reuse=None,
    renorm=False,
    renorm_clipping=None,
    renorm_momentum=0.99,
    fused=None,
    virtual_batch_size=None,
    adjustment=None
)
```

`axis`的值取决于按照`input`的哪一个维度进行BN，例如输入为`channel_last` format，即`[batch_size, height, width, channel]`，则`axis`应该设定为4，如果为`channel_first` format，则`axis`应该设定为1.

`momentum`的值用在训练时，滑动平均的方式计算滑动平均值`moving_mean`和滑动方差`moving_variance`。 后面做更详细的说明。

`center`为`True`时，添加位移因子`beta`到该BN层，否则不添加。添加`beta`是对BN层的变换加入位移操作。注意，`beta`一般设定为可训练参数，即`trainable=True`。

`scale`为`True`是，添加缩放因子`gamma`到该BN层，否则不添加。添加`gamma`是对BN层的变化加入缩放操作。注意，`gamma`一般设定为可训练参数，即`trainable=True`。

`training`表示模型当前的模式，如果为`True`，则模型在训练模式，否则为推理模式。要非常注意这个模式的设定，这个参数默认值为`False`。如果在训练时采用了默认值`False`，则滑动均值`moving_mean`和滑动方差`moving_variance`都不会根据当前batch的数据更新，这就意味着在推理模式下，均值和方差都是其初始值，因为这两个值并没有在训练迭代过程中滑动更新。





## 参考

- [详解深度学习中的Normalization，BN/LN/WN](https://zhuanlan.zhihu.com/p/33173246)
- [深度学习中的Normalization模型](http://old-101.cvmart.net/community/article/detail/368)
- [Batch Normalization的正确打开方式](https://www.jianshu.com/p/437fb1a5823e)：关于后记部分，还是没有读懂

