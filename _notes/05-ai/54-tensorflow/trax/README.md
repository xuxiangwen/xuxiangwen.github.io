Trax是一个极简的开源深度学习框架，它专注于清晰的代码和速度，被Google Brain Team维护。 Trax 代码分为下面几个部分。

## [Trax_Quick_Intro.ipynb](http://15.15.175.163:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/trax/Trax_Quick_Intro.ipynb)

介绍了Trax里面的内容。

- **fastmath/：**最基本的数学运算，以及通过 JAX 和 TensorFlow 加速运算性能的方法，尤其是在 GPU/TPU 上；

  使用[JAX](https://github.com/google/jax)作为数学计算的包。

  JAX是一个函数转换的集合，例如实时编译和自动微分，它是用一个API在XLA上实现的瘦包装器，API本质上是NumPy和SciPy的替代品。事实上，开始使用JAX的一种方法是将其视为一个加速器支持的NumPy。

  ~~~python
  from trax.fastmath import numpy as fastnp
  trax.fastmath.use_backend('jax')  # Can be 'jax' or 'tensorflow-numpy'.
  ~~~

- **layers/：**搭建神经网络的所有层级构建块；

- **models/：**包含所有基础模型，例如 MLP、ResNet 和 Transformer，还包含一些前沿 DL 模型；

- **optimizers/：**包含深度学习所需要的最优化器；

- **supervised/：**包含执行监督学习的各种有用模块，以及整体的训练工具；

- **rl/：**包含谷歌大脑在强化学习上的一些研究工作；

## [layers_intro.ipynb](http://15.15.175.163:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/trax/layers_intro.ipynb)

## [Using_Trax_with_Keras.ipynb](http://15.15.175.163:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/trax/Using_Trax_with_Keras.ipynb)

