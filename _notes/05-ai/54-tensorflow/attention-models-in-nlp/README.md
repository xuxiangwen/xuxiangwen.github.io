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







示例

### [C4_W1_Assignment.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/attention-models-in-nlp/Week_1/C4_W1_Assignment.ipynb)



### [C4_W1_Assignment_Solution.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/attention-models-in-nlp/Week_1/C4_W1_Assignment_Solution.ipynb)

