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





### [C4_W1_Ungraded_Lab_Bleu_Score.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/attention-models-in-nlp/Week_1/C4_W1_Ungraded_Lab_Bleu_Score.ipynb)



### [C4_W1_Assignment.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/attention-models-in-nlp/Week_1/C4_W1_Assignment.ipynb)



### [C4_W1_Assignment_Solution.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/attention-models-in-nlp/Week_1/C4_W1_Assignment_Solution.ipynb)

