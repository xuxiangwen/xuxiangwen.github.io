---
title: LDA模型
categories: statistics
date: 2020-08-23
---

在NLP领域，LDA（Latent Dirichlet Allocation）是非常著名的算法，它是由[David M. Blei](http://www.cs.columbia.edu/~blei/)、[Andrew Ng](https://zh.wikipedia.org/wiki/吴恩达)和[Michael I. Jordan](https://zh.wikipedia.org/wiki/迈克尔·乔丹_(学者))于2003年提出。

![image-20200816083028876](images/image-20200816083028876.png)

LDA算法在文本主题识别、文本分类以及文本相似度计算方面得到广泛的运用，同时它也有很深刻的数学背景，所以非常值得大家进行深入的学习。它有如下特点：

- 它是一个主题模型。它将每篇文档的主题以概率分布的形式给出。
- 它是一个无监督模型，不需要人工标记书，所以该算法得到广泛的运用。
- 它是一个生成模型。 它假定每篇文章中的每个词是由背后的一个潜在的主题中抽取出来：

## 模型概述

![image-20200817083349545](images/image-20200817083349545.png)

上图是LDA的概率图模型表示图。图中的阴影圆圈表示可观测变量（observed variable），非阴影圆圈表示潜在变量（latent variable），箭头表示两变量间的条件依赖性（conditional dependency），方框表示重复抽样，重复次数在方框的右下角。

- $M $代表训练语料中的文章数；
- $K$ 代表设置的主题数；
- $V $代表训练语料中的所有单词数，
- $N $代表文章中的单词数， $N_i$代表第$i$篇文章的单词数；
- $\theta $是一个$M\times K$ 的矩阵， $ {\theta}_m$代表第$m$篇文章的主题分布；
- $\varphi$ 是一个$K \times V $的矩阵，$ {\varphi}_k$代表编号为 $k$的主题之上的词分布；
- $\alpha $ 是每篇文档的主题分布的先验分布Dirichlet 分布的参数（也被称为超参
  数），其中$ \theta_i \sim  Dir( \alpha)$；
- $\beta$是每个主题的词分布的先验分布Dirichlet 分布的参数（也被称为超参
  数），其中$ \varphi_k \sim  Dir( \beta)$；
- $w$是可被观测的词，$w_{ij}$表示第$i$篇文章的第$j$个单词；
- $z$是每个对于被观测的词的潜在的主题分配，$z_{ij} $表示第$i$篇文章的第$j$个单词所属的主题。

整个生成过程如下：

- a. 生成$ \theta_m  \sim  Dir( \alpha)$，其中$i \in \{1,2, \cdots, M\}$；
- b. 生成$ \varphi_k \sim  Dir( \beta)$，其中$k \in \{1,2, \cdots, K\}$；
- 生成第$i$篇文章的第$j$个单词，其中$i \in \{1, 2, \cdots, M\} , j \in \{1, 2, \cdots, N_i\}$：
  - c. 从多项分布$Multinomial(\theta_i)$取样，获得一个topic主题$z_{ij} $。
  - d. 从多项分布$ Multinomial(\varphi_{z_{ij}})$取样，获得一个单词$w_{ij} $。

为了更加形象的理解，可以把整个过程看成是扔色子。

![image-20200817093845405](images/image-20200817093845405.png)

- $a$过程：根据$Dir( \alpha)$分布，生成$M$个文章的主题色子，每个色子有$K$个面；
- $b$过程：根据$Dir( \beta)$分布，生成$K$个主题的单词色子，每个色子有$V$个面；
- $c$过程：对于每一个单词，投掷其所在文章对应的色子，获得一个主题$z_{ij}$；
- $d$过程：通过$z_{ij}$获得一个单词色子，然后投掷，获得一个单词。



### 联合概率

$$
\begin{align}
y &= x + 5 \\
&= 3 + 5 \\
&= 8
\end{align}
$$



由于，$\alpha$和$ w$相互独立，$ \beta$和$z $相互独立，可以得到下面的联合分布。
$$
\begin{align}
p( w,  z\vert  \alpha, \beta) &=  p( w \vert  z, \alpha, \beta) p( z \vert  \alpha, \beta) 
\\ & = 
 p( w \vert  z,   \beta) p( z \vert   \alpha ) 
\end{align}
$$
下面来求解$ p( w \vert  z,   \beta) $和$p( z \vert   \alpha ) $：
$$
\begin{align}
p( w \vert  z,  \beta)  = 1
\end{align}
$$

$$
\begin{align}
y &= x + 5 \\
&= 3 + 5 \\
&= 8
\end{align}
$$



## 预备知识

### Beta分布和

## 从最大似然到贝叶斯



## Unigram Model

下面回到我们要解决的问题。Unigram Model假设所有单词的产生都



### 最大似然估计



### 贝叶斯估计



## Topic Model



### PLSA



### LDA



## 参考

- [Latent Dirichlet Allocation漫游指南](https://arxiv.org/ftp/arxiv/papers/1908/1908.03142.pdf)

- [LDA数学八卦](https://bloglxm.oss-cn-beijing.aliyuncs.com/lda-LDA%E6%95%B0%E5%AD%A6%E5%85%AB%E5%8D%A6.pdf)

- [Paper: Latent Dirichlet Allocation](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf)

- [LDA学习笔记(4) – Gibbs Sampling 推导](https://carlhwang1989.wordpress.com/2015/02/18/lda%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B04-2/)

  



