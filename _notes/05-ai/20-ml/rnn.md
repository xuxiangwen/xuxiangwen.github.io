## RNN

![img](images/20150915110014414)

![一份详细的LSTM和GRU图解](images/1_AQ52bwW55GsJt6HTxPDuMA.gif)

![一份详细的LSTM和GRU图解](images/1_o-Cq5U8-tfa1_ve2Pf3nfg.gif)

![一份详细的LSTM和GRU图解](images/1_WMnFSJHzOloFlJHU6fVN-g.gif)

#### 总参数数量

shape(h)× [shape(h)+shape(x)] + shape(h) 

## LSTM

Long Short-Term Memory（长短期记忆网络）L的核心概念是Cell States和各种Gates。Cell State在整个序列的处理过程中都携带相关的信息，即使较早时刻的信息也可以很好的保留，从而降低了短期记忆问题的影响。从图中可以看到有两条线，一条是Hidden State （$h_t$），一条是Cell State（$c_t$）。

**LSTM 是个奇葩**：它的状态是 (c, h) 这样一个 pair，其中 c 用于存储一些信息，而 h 用于上层输出。这里 (c, h) 分离的直觉，我称之为**信息隐匿**：

- 让 c 在一条高速公路上行进（相邻时间步的 c 只有加性更新，没有非线性变换）有利于保持信息在跨越多个时间步后仍然清晰可辨。
- 又因为模型当前的输出可能并不需要它记住的所有历史信息，而是只跟其中一部分信息有关，所以 h 用于把 c 中和当前输出相关的部分提取出来。

![img](images/20150915110046267)

![img](images/10-1024x613.png)

![img](images/7239122-6cc9c9fd5b2861c8.png)

### Forget Gate

Forget Gate决定哪些信息需要丢弃，哪些信息需要保留。它合并前一个Hidden State和当前的Input信息，然后输入Sigmoid激活函数，输出(0,1)之间的数值。输出值接近0的信息需要被遗忘，输出值接近1的信息需要被保留。

![img](images/20150915121435938)

![img](images/12.gif)

### Input Gate

Input Gate首先将前一个Hidden State和当前Input合并起来，送入Sigmoid函数，输出(0,1)之间的值，0表示信息不重要，1表示信息重要。Hidden State和Input的输入同时也被送入Tanh函数，输出(-1, 1)之间的数值。

Sigmoid的输出和Tanh的输出相乘，决定哪些Tanh的输出信息需要保留，哪些输出信息需要丢弃。

![img](images/20150915121744590)

![img](images/13.gif)

### Cell State: 将过去与现在的记忆进行合并

前一个Cell State的输出，首先与Forget Gate的输出相乘，选择性的遗忘不重要的信息，再与Input Gate的输出相加，从而实现将当前的Input信息添加到Cell State中，输出新的Cell State。

![image-20201212201518975](images/image-20201212201518975.png)

### Output Gate

Output Gate用于输出Hidden State。Output Gate首先将前一个Hidden State和当前Input送入Sigmoid函数，然后与新的Cell State通过Tanh函数的输出相乘，决定Hidden State要将哪些信息携带到下一个Time Step。

![img](images/20150915121942641)

![img](images/15.gif)

### 参数计算

~~~python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM

model = Sequential([Embedding(500, 16, input_length=128), 
                    LSTM(32)])
model.summary()
~~~

![image-20201212224333296](images/image-20201212224333296.png)



## GRU

GRU与LSTM非常相似，但它去除了Cell State，使用Hidden State来传递信息。GRU只有两个Gates: Reset Gate和Update Gate。

![img](images/17-1024x835.png)

上图不够直接明白，再来一张台湾大学李宏毅教学视频中的讲解

![img](images/18-1024x957.jpg)

其中$x^t$和$h^{t−1}$是GRU的输入，$y^t$和$h^t$是GRU的输出。

![img](images/19.jpg)

如上图所示，r是Reset Gate，z为Update Gate。
$$
h^{t-1^{\prime}}=h^{t-1} \odot r
$$


![img](images/20.jpg)

再将${h^{t−1}}^{'}$与$x^t$进行拼接，送入Tanh激活函数得到$h^{'}$。

最后进行**记忆更新**的步骤：
$$
h^{t}=(1-z) \odot h^{t-1}+z \odot h^{\prime}
$$
Update Gate: z的范围为0~1，它的值越接近1，代表记忆数据越多；它的值越接近0，则代表遗忘的越多。

### Stacked LSTM

![preview](images/v2-e77a5a96718c52a0f890e3bf1a77f731_r.jpg)





## Stateful RNN

有状态的RNN能够在训练中维护跨批次的有状态信息，即当前批次的训练数据计算的状态值，可以用作下一批次训练数据的初始隐藏状态。stateful代表除了每个样本内的时间步内传递，而且每个样本之间会有信息(c,h)传递。

- 优点：更小的网络，或者更少的训练时间

- 缺点：需要数据batchsize来训练网络，并在每个训练epoch后重置状态，

实现步骤：

1. 必须将batch_size参数显式的传递给模型的第一层
2. 在RNN层中设置stateful=True
3. 在调用fit()时指定shuffle=False，打乱样本之后，sequence之间就没有依懒性了。
4. 训练完一个epoch后，要重置状态
   - 使用 model.reset_states()来重置模型中所有层的状态。
   - 使用layer.reset_states()来重置指定有状态 RNN 层的状态

有两种方式：

- LSTM(hidden_size, stateful=True, batch_input_shape=(batch_size, timestep, input_dim))

- LSTM(hidden_size, stateful=True, input_shape=(data[1], data[2]), batch_size)

## 参数和output计算

~~~python

~~~

 

## 参考

- [一份详细的LSTM和GRU图解](http://www.atyun.com/30234.html)

- [RNN、lstm、gru详解](https://www.cnblogs.com/AntonioSu/p/8798960.html)：解释的非常清楚。

- [动图详解LSTM和GRU](http://www.banbeichadexiaojiubei.com/index.php/2020/06/26/%E5%8A%A8%E5%9B%BE%E8%AF%A6%E8%A7%A3lstm%E5%92%8Cgru/)

- [LSTM模型详解](https://blog.csdn.net/hust_tsb/article/details/79485268)

- [门控循环单元（GRU）](https://zh.d2l.ai/chapter_recurrent-neural-networks/gru.html):讲解的很清楚，就是图很难看。

- [Keras中的LSTM](https://www.jianshu.com/p/3edff278f021)

- [从RNN到BERT](https://www.cnblogs.com/wkang/p/13397636.html)  

- [LSTM 的奇葩设计](https://zhuanlan.zhihu.com/p/34500721)

- [Keras实现RNN模型](https://www.cnblogs.com/LXP-Never/p/10940123.html)

  

