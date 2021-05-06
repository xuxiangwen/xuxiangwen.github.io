本课程来自Coursera上的课程[Getting started with TensorFlow 2](https://www.coursera.org/learn/getting-started-with-tensor-flow2/home/welcome)，是系列课程[TensorFlow 2 for Deep Learning Specialization](https://www.coursera.org/specializations/tensorflow2-deeplearning)的第一个课程。

### Week 1：Sentiment Analysis with Logistic Regression

#### [NLP_C1_W1_lecture_nb_01.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/classification-vector-spaces-in-nlp/NLP_C1_W1_lecture_nb_01.ipynb)

对nltk.corpus.twitter_samples中的twitter数据集进行情感分类（正面positive和负面negative）。在构建模型之前，首先要对文本数据进行预处理。

- 使用正则表达式去除一些字符

  比如：hyperlinks，#，RT

- 使用nltk.tokenize.TweetTokenizer把字符串分成words

- 使用nltk.corpus.stopwords去除stopwords

- 使用string.punctuation移除标点符号（punctuation）

- 使用nltk.stem.PorterStemmer进行词根替换

上述代码参见[utils.py](http://15.15.166.35:18888/edit/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/classification-vector-spaces-in-nlp/week1/utils.py)。

#### [NLP_C1_W1_lecture_nb_02.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/classification-vector-spaces-in-nlp/NLP_C1_W1_lecture_nb_02.ipynb)

面对情感分类问题，我们往往会统计文本中正面词汇和负面词汇的个数，那么如何获取正面词汇和负面词汇呢？最简单的方法是，分别统计一个词汇在正面文本和负面文本中出现的次数。根据这两个指标，可以可视化words，得到如下图形。

![image-20210429144926423](images/image-20210429144926423.png)

可以很明显看出， `:)` 代表强烈的正面情感，而 `:(`代表强烈的负面情感。在文本处理中，要避免把这样类似的word移除。

> 上面这种获得词向量的方式，虽然简单，但也是有效的方法之一。

#### [NLP_C1_W1_lecture_nb_03.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/classification-vector-spaces-in-nlp/NLP_C1_W1_lecture_nb_03.ipynb)

根据前两个notebook所说的处理方式，处理twitter模型，然后可视化Logistic Regression的边界。其中theta调用了C1_W1_Assignment中训练后的结果

![image-20210429174609083](images/image-20210429174609083.png)

#### [C1_W1_Assignment.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/classification-vector-spaces-in-nlp/C1_W1_Assignment.ipynb)

完整展示了Logistic Regression的实现过程，非常不错。尤其是一些公式。

* $\mathbf{\theta}$ has dimensions (n+1, 1), where 'n' is the number of features, and there is one more element for the bias term $\theta_0$ (note that the corresponding feature value $\mathbf{x_0}$ is 1).
$$\mathbf{\theta} = \begin{pmatrix}
\theta_0
\\
\theta_1
\\ 
\theta_2 
\\ 
\vdots
\\ 
\theta_n
\end{pmatrix}$$
* The 'logits', 'z', are calculated by multiplying the feature matrix 'x' with the weight vector 'theta'.  $z = \mathbf{x}\mathbf{\theta}$
    * $\mathbf{x}$ has dimensions (m, n+1) 
    * $\mathbf{\theta}$: has dimensions (n+1, 1)
    * $\mathbf{z}$: has dimensions (m, 1)
* The prediction 'h', is calculated by applying the sigmoid to each element in 'z': $h(z) = sigmoid(z)$, and has dimensions (m,1).
* The cost function $J$ is calculated by taking the dot product of the vectors 'y' and 'log(h)'.  Since both 'y' and 'h' are column vectors (m,1), transpose the vector to the left, so that matrix multiplication of a row vector with column vector performs the dot product.
$$J = \frac{-1}{m} \times \left(\mathbf{y}^T \cdot log(\mathbf{h}) + \mathbf{(1-y)}^T \cdot log(\mathbf{1-h}) \right)$$
* The update of theta is also vectorized.  Because the dimensions of $\mathbf{x}$ are (m, n+1), and both $\mathbf{h}$ and $\mathbf{y}$ are (m, 1), we need to transpose the $\mathbf{x}$ and place it on the left in order to perform matrix multiplication, which then yields the (n+1, 1) answer we need:
$$\mathbf{\theta} = \mathbf{\theta} - \frac{\alpha}{m} \times \left( \mathbf{x}^T \cdot \left( \mathbf{h-y} \right) \right)$$



### Week2: Sentiment Analysis with Naïve Bayes

朴素贝叶斯训练步骤：

1. 加载文本数据。

2. 文本预处理：process_tweet(tweet)

    - Lowercase
    - Remove punctuation, urls, names
    - Remove stop words
    - Stemming
    - Tokenize sentences

3.  计算 freq(w, class)。

    ![img](images/MmWbHT6RTwGlmx0-kS8BxA_679ede84d1f64f3ebb9b52957e40c037_Screen-Shot-2020-09-08-at-4.33.37-PM.png)

4. 计算 $$P(w | pos), P(w | neg)  $$。

    采用拉普拉斯平滑（Laplacian Smoothing）。

    $$
    P\left(\mathrm{w}_{\mathrm{i}} \mid \mathrm{class}\right)=\frac{\operatorname{freq}\left(\mathrm{w}_{\mathrm{i}}, \text { class }\right)+1}{\left(\mathrm{N}_{\text {class }}+\mathrm{V}\right)}
    $$

    其中：$$N_{class}$$表示所有单词出现的频次，$$V$$表示不同词汇的个数。

3. 计算 $$\lambda (w)$$。

    $$ \lambda(w)=\log \frac{P(\mathrm{w} \mid \mathrm{pos})}{P(\mathrm{w} \mid \mathrm{neg})}$$

6. 计算先验概率 $$log(prior) = \log(P(pos) / P(neg))=\log \frac{D_{p o s}}{D_{n e g}}$$。

    其中$$D_{pos}$$,$$D_{neg}$$分别代表正面文档和负面文档的数量。 

#### [NLP_C1_W2_lecture_nb_01.ipynb](http://15.15.166.35:18888/notebooks/eipi10/xuxiangwen.github.io/_notes/05-ai/54-tensorflow/classification-vector-spaces-in-nlp/NLP_C1_W2_lecture_nb_01.ipynb)

