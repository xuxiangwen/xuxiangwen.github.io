# [Natural Language Processing with Attention Models](https://www.coursera.org/learn/attention-models-in-nlp/home/welcome)

## Week 1: Neural Machine Translation

### Seq2seq to Attention 

Attention模型原理参见 [attention.md](..\..\20-ml\attention.md) 

Attention中的Key， Value来自Encoder的Hidden States，而Query来自Decoder的Hidden States

![img](images/tVlC8-qdTRWZQvPqnV0VKg_c3fce0ddebb94d8eb15ca2cc19348b8e_Screen-Shot-2020-11-05-at-11.26.53-AM.png)

基本公式如下：
$$
Attention = Softmax(\mathbf {QK^T})\mathbf V
$$
从下图中，可以看出各个词语之间的权重。

![img](images/luf7KWwaT2Sn-ylsGg9kkA_dbebeeb223ca43b3bb05baad8795230b_Screen-Shot-2020-11-05-at-12.55.01-PM.png)



### NMT（Neural Machine Translation）

![img](images/Lt8Btwk1TdSfAbcJNb3UZA_c2c506c3a6e54ba480ffbb65edff158f_Screen-Shot-2020-11-05-at-1.56.47-PM.png)

- input表示为0， target表示为1。

  input和target都被复制了一份（Select([0, 1, 0, 1])）。input的第一份传给input encoder，另外一份传给input encoder。target的一份传给pre-attention decoder，另外一份传给了Select([0, 2])

- input encoder: 输入input，输出K，V

- pre-attention decoder：输入target，输出Q

  采用了[teacher forcing](https://blog.csdn.net/qq_30219017/article/details/89090690)

### Sampling and Decoding

在encoder完成hidden state的计算后，decoder开始来预测下一个token。decoder使用一定策略来生成这个token。常用的方法有：

- Greedy decoding

  每次选择概率最大的词。

- Random Sampling

  - Temperature 

- Beam Search

  首先需要确定一个`Beam Size`，这里设置为2，意思是每个`word`后面的分支考虑概率最大的那两个`words`。比如下面的例子，从下往上首先分成A、B两个words，然后继续往上传播，句子变成是AA/AB/BA/BB这四种情况（绿色虚线）。考虑到`Beam Size=2`，选择概率最大的两个，假设是AB/BA（橙色大箭头）。然后以选择的AB/BA继续向上传播，又出现了四种情况ABA/ABB/BBA/BBB，依然是选择综合概率最大的两个ABB/BBB。以此类推，直至句子结束。只要可以调整好`Beam Size`，就能够使用最小的计算量，得到最优的结果。

  ![img](images/v2-bd114c9037cc4ac7fb8936a18807cc4e_720w.jpg)

- 最小贝叶斯风险（Minimum Bayes Risk）

  还未完全理解。

  ![image-20210608152616145](images/image-20210608152616145.png)



### [C4_W1_Ungraded_Lab_Stack_Semantics.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/attention-models-in-nlp/Week_1/C4_W1_Ungraded_Lab_Stack_Semantics.ipynb)

主要介绍 [Trax](../trax/README.md) 的Stack（栈）的特性。

![image-20210604115805268](images/image-20210604115805268.png)

对应代码如下：

~~~python
serial = tl.Serial(
    tl.Select([0, 1, 0, 1]), Addition(), Multiplication(), Addition(), tl.Residual()
)

# Initialization
x = (np.array([3]), np.array([4]))  # input

serial.init(shapes.signature(x))  # initializing serial instance

print("-- Serial Model --")
print(serial, "\n")
print("-- Properties --")
print("name :", serial.name)
print("sublayers :", serial.sublayers)
print("expected inputs :", serial.n_in)
print("promised outputs :", serial.n_out, "\n")

# Inputs
print("-- Inputs --")
print("x :", x, "\n")

# Outputs
y = serial(x)
print("-- Outputs --")
print("y :", y)
~~~

> 对于Stack这种特性，究竟有啥好处呢，目前还不能理解。

### [C4_W1_Ungraded_Lab_Bleu_Score.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/attention-models-in-nlp/Week_1/C4_W1_Ungraded_Lab_Bleu_Score.ipynb)

BLEU的介绍参见 [bleu.md](..\..\20-ml\bleu.md) 

在本例中，对于不同n-gram，采用了相同的系数$1/4$。
$$
BLEU = BP\Bigl(\prod_{i=1}^{4}p_i\Bigr)^{(1/4)}
$$

$$
BP = min\Bigl(1, e^{(1-( {r}/{c}))}\Bigr)
$$

$$
p_i = \frac {\sum_{snt \in{cand}}\sum_{i\in{snt}}min\Bigl(m^{i}_{cand}, m^{i}_{ref}\Bigr)}{w^{i}_{t}}
$$

where:

* $m^{i}_{cand}$, is the count of i-gram in candidate matching the reference translation.
* $m^{i}_{ref}$, is the count of i-gram in the reference translation.
* $w^{i}_{t}$, is the total number of i-grams in candidate translation.

在示例中，手工实现了句子层面的BLEU，**只是其中Candidate和Reference好像搞反了**。另外程序调用了`sacrebleu.corpus_bleu`来比较手工实现的结果。

### [C4_W1_Assignment.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/attention-models-in-nlp/Week_1/C4_W1_Assignment.ipynb)

下面是几个关键技术的讲解。

#### Bucketing

提高模型训练速度的一种方式。根据句子的长度，把句子分到不同的bucket。每个bucket根据最长句子进行补齐，训练时，每个batch的随机选择一个bucket，然后从中加载数据。

![alt text](https://miro.medium.com/max/700/1*hcGuja_d5Z_rFcgwe9dPow.png)

对于不同的bucket，还可以指定不同的batch_size。比如：

~~~python
boundaries =  [8,   16,  32, 64, 128, 256, 512]
batch_sizes = [256, 128, 64, 32, 16,    8,   4,  2]
~~~

- 如果$sentence\_length\leq8$， 则$batch\_size=256$
- 如果$8< sentence\_length\leq 16$， 则$batch\_size=256$
- 如果$512 < sentence\_length$， 则$batch\_size=2$

#### Attention

![image-20210609135729224](images/image-20210609135729224.png)
$$
Attention(Q, K, V) = softmax(\frac{QK^T}{\sqrt{d_k}})V
$$


#### Padding Mask

因为每个批次输入序列长度是不一样的也就是说，我们要对输入序列进行对齐。具体来说，就是给在较短的序列后面填充 0。但是如果输入的序列太长，则是截取左边的内容，把多余的直接舍弃。因为这些填充的位置，其实是没什么意义的，所以我们的attention机制不应该把注意力放在这些位置上，所以我们需要进行一些处理。

具体的做法是，把这些位置的值加上一个非常大的负数(负无穷)，这样的话，经过 softmax，这些位置的概率就会接近0！

而我们的 padding mask 实际上是一个张量，每个值都是一个Boolean，值为 false 的地方就是我们要进行处理的地方。

设$m$表示target的长度， $n$表示input的长度，$$Q = \begin{bmatrix} q_1^{T} \\ q_2^{T} \\ \vdots \\ q_m^{T} \end{bmatrix}$$，$$K^{T} = \begin{bmatrix} v_1 & v_2 & \cdots & v_n \end{bmatrix}$$

则target中第$i$个token的Attention可以表示为：
$$
\begin{align}
Attention(q_i, K, V) &= softmax(\frac{q_i^{T}K^T}{\sqrt{d_k}})V \\
&=  softmax \left( \frac {\begin{bmatrix} q_i^{T}v_1 & q_i^{T}v_2 & \cdots & q_i^{T}v_n \end{bmatrix}} {\sqrt{d_k}} \right)V
\end{align}
$$
因此在





## 课程资源

可以逐步阅读一下，以下的论文。

- [Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer](https://arxiv.org/abs/1910.10683) (Raffel et al, 2019)

 - [Reformer: The Efficient Transformer](https://arxiv.org/abs/2001.04451) (Kitaev et al, 2020)

 - [Attention Is All You Need](https://arxiv.org/abs/1706.03762) (Vaswani et al, 2017)

 - [Deep contextualized word representations](https://arxiv.org/pdf/1802.05365.pdf) (Peters et al, 2018)

 - [The Illustrated Transformer](http://jalammar.github.io/illustrated-transformer/) (Alammar, 2018)

 - [The Illustrated GPT-2 (Visualizing Transformer Language Models)](http://jalammar.github.io/illustrated-gpt2/) (Alammar, 2019)

 - [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805) (Devlin et al, 2018)

 - [How GPT3 Works - Visualizations and Animations](http://jalammar.github.io/how-gpt3-works-visualizations-animations/) (Alammar, 2020)
