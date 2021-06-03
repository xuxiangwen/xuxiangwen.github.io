# [Natural Language Processing with Attention Models](https://www.coursera.org/learn/attention-models-in-nlp/home/welcome)

## Week 1: Neural Machine Translation

Attention模型原理参见 [attention.md](..\..\20-ml\attention.md) 

Attention中的Key， Value来自Encoder的Hidden States，而Query来自Decoder的Hidden States

![img](images/tVlC8-qdTRWZQvPqnV0VKg_c3fce0ddebb94d8eb15ca2cc19348b8e_Screen-Shot-2020-11-05-at-11.26.53-AM.png)

基本公式如下：
$$
Attention = Softmax(\mathbf {QK^T})\mathbf V
$$
从下图中，可以看出各个词语之间的权重。

![img](images/luf7KWwaT2Sn-ylsGg9kkA_dbebeeb223ca43b3bb05baad8795230b_Screen-Shot-2020-11-05-at-12.55.01-PM.png)

### [C4_W1_Ungraded_Lab_Stack_Semantics.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/attention-models-in-nlp/Week_1/C4_W1_Ungraded_Lab_Stack_Semantics.ipynb)

用到了谷歌大脑开源[Trax](https://github.com/google/trax)代码库。Trax是一个极简的开源深度学习框架，它专注于清晰的代码和速度，被Google Brain Team维护。 Trax 代码分为下面几个部分。

- **fastmath/：**最基本的数学运算，以及通过 JAX 和 TensorFlow 加速运算性能的方法，尤其是在 GPU/TPU 上；
- **layers/：**搭建神经网络的所有层级构建块；
- **models/：**包含所有基础模型，例如 MLP、ResNet 和 Transformer，还包含一些前沿 DL 模型；
- **optimizers/：**包含深度学习所需要的最优化器；
- **supervised/：**包含执行监督学习的各种有用模块，以及整体的训练工具；
- **rl/：**包含谷歌大脑在强化学习上的一些研究工作；

Trax的快速入门见[Trax Quick Intro](https://colab.research.google.com/github/google/trax/blob/master/trax/intro.ipynb)。



### [C4_W1_Ungraded_Lab_Bleu_Score.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/attention-models-in-nlp/Week_1/C4_W1_Ungraded_Lab_Bleu_Score.ipynb)



### [C4_W1_Assignment.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/attention-models-in-nlp/Week_1/C4_W1_Assignment.ipynb)



### [C4_W1_Assignment_Solution.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/attention-models-in-nlp/Week_1/C4_W1_Assignment_Solution.ipynb)

