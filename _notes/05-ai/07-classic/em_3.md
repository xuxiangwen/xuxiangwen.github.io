---
title: EM算法实践：聚类
categories: algorithm
date: 2020-07-31
---

[EM](https://zh.wikipedia.org/wiki/%E6%9C%80%E5%A4%A7%E6%9C%9F%E6%9C%9B%E7%AE%97%E6%B3%95)（Expectation-Maximum）算法在机器学习中有极为广泛的用途。为了能够加深理解，本文将运用EM算法原理来分析两个经典的聚类模型：K-Means和GMM。

开始之前，再次复习KM算法的流程。

- 输入：观察数据$x=(x_1,x_2,...x_m)$，联合分布$P(x,z;θ)$, 条件分布$P(z\vert x;θ)$, 最大迭代次数$J$。

- 目标函数
  $$
  L(\theta) = \sum\limits_{i=1}^m \log\sum\limits_{z_{i}}P(x_{i}, z_{i};\theta) 
  \\ \theta = arg \max \limits_{\theta}\sum\limits_{i=1}^mL(\theta)
  $$

- 算法：

  1. 随机初始化模型参数$\theta$的初值$\theta^1$。

  2. for $j$  from $1$ to $J$开始EM算法迭代：

     - E步：计算联合分布的条件概率期望：
       $$
       \begin{align}
       Q_i(z_{i}) = P( z_{i}|x_{i};\theta^{j}), \ \ \  \sum\limits_{z_{i}}Q_i(z_{i}) =1
       \\ L(\theta, \theta^{j}) = \sum\limits_{i=1}^m\sum\limits_{z_{i}}Q_i(z_{i})\log \frac {P(x_{i}, z_{i};\theta)} {Q_i(z_{i})} 
       \end{align}
       $$

     - M步：极大化$L(\theta, \theta^{j})$, 得到$\theta^{j+1}$：
       $$
       \theta^{j+1} = arg \max \limits_{\theta}L(\theta, \theta^{j})
       $$

     - 如果$\theta^{j+1}$已收敛，则算法结束。否则继续回到E步进行迭代。

- 输出：模型参数$\theta$。

## K-Means

[K-Means](https://zh.wikipedia.org/wiki/K-%E5%B9%B3%E5%9D%87%E7%AE%97%E6%B3%95)算法是最经典的聚类算法，K-Means把$m$个样本划分到$K $个簇中，一个簇有一个簇中心，一个样本属于离它最近的簇（通过计算样本到簇中心的距离来比较）。算法的目的是，让簇内的点尽量紧密的连在一起，而让簇间的距离尽量的大。它的数学定义如下：

假设簇划分为$(C_1,C_2,...C_K)$，则我们的目标是最小化平方误差$E$：
$$
E = \sum\limits_{i=1}^K\sum\limits_{x \in C_i} ||x-\mu_i||^2
$$
其中$\mu$是簇$C_i$的中心，也称为质心，是属于该簇样本的均值，其计算公式为：$\mu_i = \frac{1}{\vert C_i \vert}\sum\limits_{x \in C_i}x$。

### 定义

- 设$\gamma=(\gamma_1,\gamma_2,...\gamma_m)$，表示每个点属于哪一个簇。其中$\gamma_i$是一个长度为$K$的向量，它只有一个成员是1，其它都是0。$\gamma$相当于经典EM算法中的隐变量$z$。

- 设$\theta=(\mu_1, \mu_2, \cdots, \mu_K)$，则可以推出：
  $$
  \begin{align}
  E(\theta) = \sum_i^m\sum_k^K\gamma_{ik}(x_i-\mu_k)^2
  \\ 
  \theta = arg \min \limits_{\theta}\sum\limits_{i=1}^mE(\theta)
  \end{align}
  $$
  显然，对于任意的$\theta$，要满足上面的公式，$\gamma$必然满足
  $$
  \gamma_{ik} =
  \begin{equation} 
  \left\{
  \begin{array}{lcl} 
  1 &  & if \ k = arg \min \limits_{l} (x_i - \mu_l)^2 \\
  0 &  & otherwise
  \end{array}  
  \right.
  \end{equation}
  $$

### 流程

显见，上面目标函数和经典EM算法有些不同，这是因为经典EM算法其目标函数来自于极大似然估计，而K-Means聚类中，没有极大似然估计，没有$log$，不需要用Jessen不等式了，它的$E(\theta)$直接就是基于隐变量分布的表示，总体上大大简化了。流程更新如下。

- 输入：观察数据$x=(x_1,x_2,...x_m)$，最大迭代次数$J$。

- 目标函数
  $$
  \gamma_{ik} =
  \begin{equation} 
  \left\{
  \begin{array}{lcl} 
  1 &  & if \ k = arg \min \limits_{l} (x_i - \mu_l)^2 \\
  0 &  & otherwise
  \end{array}  
  \right.
  \end{equation}
  $$

  $$
  \begin{align}
  E(\theta) = \sum_i^m\sum_k^K\gamma_{ik}(x_i-\mu_k)^2   
  \\ 
  \theta = arg \min \limits_{\theta}\sum\limits_{i=1}^mE(\theta)   
  \end{align}
  $$

- 算法：

  1. 随机初始化模型参数$\theta$的初值$\theta^1=(\mu_1^1, \mu_2^1, \cdots, \mu_K^1)$。

  2. for $j$  from $1$ to $J$开始EM算法迭代：

     - E步：
       $$
       \gamma_{ik}^j =
       \begin{equation} 
       \left\{
       \begin{array}{lcl} 
       1 &  & if \ k = arg \min \limits_{l} (x_i - \mu_l^j)^2 \\
       0 &  & otherwise
       \end{array}  
       \right.
       \end{equation}
       $$

       $$
       \begin{align}
       \\ E(\theta, \theta^{j}) =  \sum_i^m\sum_k^K\gamma_{ik}^j(x_i-\mu_k)^2
       \end{align}
       $$

     - M步：极小化$E(\theta, \theta^{j})$, 得到$\theta^{j+1}$：
       $$
       \theta^{j+1} = arg \max \limits_{\theta}E(\theta, \theta^{j})  
       $$
       通过求导，可以得到：
       $$
       \frac {\partial E(\theta, \theta^{j}) }{\partial{\mu_k}} = 2\sum_i^m\gamma_{ik}^j(x_i-\mu_k) = 0 \\
        \mu_k = \frac{\sum_i^m\gamma_{ik}^jx_n}{\sum_i^m\gamma_{ik}^j}
       $$
       很明显，属于该簇所有样本的中心便是簇中心（好像是废话）。

     - 如果$\theta^{j+1}$已收敛，则算法结束。否则继续回到E步进行迭代。

- 输出：模型参数$\theta$。

### 收敛性证明

由于和经典的EM算法有些不同，下面来再次证明收敛性，即
$$
E(\theta^{j+1}) \leq E(\theta^{j})
$$
首先，根据定义可得：
$$
E(\theta^{j+1}) = L(\theta^{j+1}, \theta^{j+1}) = \sum_i^m\sum_k^K\gamma_{ik}^{j+1}(x_i-\mu_k^{j+1})^2 \tag 1
$$
由于
$$
\gamma_{ik}^{j+1} =
\begin{equation} 
\left\{
\begin{array}{lcl} 
1 &  & if \ k = arg \min \limits_{l} (x_i - \mu_l^{j+1})^2 \\
0 &  & otherwise
\end{array}  
\right.
\end{equation}
$$
可以得到，对于一个点$x_i$，满足
$$
\sum_k^K\gamma_{ik}^{j+1}(x_i-\mu_k^{j+1})^2 <= \sum_k^K\gamma_{ik}^{j}(x_i-\mu_k^{j+1})^2
$$
把上面公式带入公式$(1)$，可得：
$$
\begin{align}
E(\theta^{j+1}) &= E(\theta^{j+1}, \theta^{j+1}) 
\\ & =
\sum_i^m\sum_k^K\gamma_{ik}^{j+1}(x_i-\mu_k^{j+1})^2 
\\ & \leq 
 \sum_i^m\sum_k^K\gamma_{ik}^{j}(x_i-\mu_k^{j+1})^2  
 \\ & =E(\theta^{j+1}, \theta^{j}) 
\\ & \leq E(\theta^{j}, \theta^{j}) & 根据公式(1)
\\ & = E(\theta^{j})
\end{align}
$$
证毕。由此可见，虽然K-Means的目标函数不同，但其求解思路和经典EM算法如出一辙，非常的巧妙。

## GMM模型

GMM（Gaussian Mixture Model） 混合高斯模型也是经典的聚类方法之一。在机器学习、计算机视觉等领域有着广泛的应用。

### 定义

- 整个分布式有$K$个高斯模型组成，设它们的均值为：$\mu=(\mu_1, \mu_2, \cdots, \mu_K)$，协方差矩阵为$\Sigma=(\Sigma_1, \Sigma_2, \cdots, \Sigma_K)$，则第k个高斯分布的概率密度可以表示为：
  $$
  \mathcal { N } ( \mathrm { x } | \mu_k , \Sigma_k ) = \frac { 1 } { ( 2 \pi ) ^ { D / 2 }  | \Sigma_k |  ^ { 1 / 2 } } \exp \left[ - \frac { 1 } { 2 } ( x - \mu_k ) ^ { T } \Sigma_k  ^ { - 1 } ( x - \mu_k ) \right]
  $$
  其中$D$表示单个样本$x$的维度，$\Sigma_k=\frac 1 m (x-\mu_k)(x-\mu_k)^T $，$\Sigma_k^{-1}$表示协方差矩阵的逆矩阵，

- 变量分布由多个高斯分布组合而成，$\pi = (\pi_1, \pi_2, \cdots, \pi_K)$表示各个高斯分布的系数（概率），且满足：
  $$
  \sum_{k=1}^K \pi_{k} =1
  $$

- 模型的参数$\theta=(\pi, \mu, \Sigma)$。

- 样本$x = (x_1,x_2,...x_m)$，根据全概率公式，每个样本的概率，可以表示为$K$个高斯分布的组合。
  $$
  P(x_i; \theta)  = \sum _ { k = 1 } ^ { K } \pi _ { k } \mathcal N ( x_i | \mu _ { k } , \Sigma _ { k } )
  $$

- 极大对数似然估计如下：
  $$
  L(\theta) =\sum _ { i = 1 } ^ { m } \log { \sum _ { k = 1 } ^ { K } \pi _ { k } N ( x _ { i } | \mu _ { k } , \Sigma _ { k } ) }
  $$
  通过极大化$L(\theta)$，来获得对应的模型参数$\theta$，即：
  $$
  \theta = arg \max \limits_{\theta}\sum\limits_{i=1}^mL(\theta)
  $$

- 隐变量设为$z=(z_1,z_2,...z_m)$，表示样本属于某个高斯分布，对于$z_i$，可以有$K$个取值，其对应的概率分布满足。
  $$
  \sum\limits_{z_{i}}Q_i(z_{i}) =1
  $$

### 算法推导

首先，随机初始化模型参数$\theta$的初值$\theta^1= (\pi^1,\mu^1,\Sigma^1)$。

然后 for $j$  from $1$ to $J$开始EM算法迭代。还是分为E步和M步

#### E步

E步将计算联合分布的条件概率期望：
$$
\begin{align}
Q_i(z_{i}) &= P( z_{i} \vert x_{i};\theta^{j})
\\ &= \frac {P( z_{i}, x_{i}; \theta^{j})} {P(x_{i}; \theta^{j})}
\end{align}
$$
$$
Q_i(z_{i}=k) =
\frac{\pi _ { k } \mathcal N ( x_i | \mu _ { k } , \Sigma _ { k } )}
{\sum _ { l = 1 } ^ { K } \pi_{ l } \mathcal N ( x_i | \mu _ { l } , \Sigma _ { l } )}
$$


  为了简化表达式，设$z_{ik}$表示$z_{i}=k$，$ \gamma_{ik} = Q_i(z_{i}=k)  $，则：
$$
\begin{align}
       L(\theta, \theta^{j}) = &
       \sum\limits_{i=1}^m\sum\limits_{z_{i}}Q_i(z_{i})\log \frac {P(x_{i},z_{i};\theta)} {Q_i(z_{i})}
       \\ =  &
       \sum\limits_{i=1}^m\sum\limits_{k=1}^K\gamma_{ik}\log \frac {P(x_{i},z_{i}=k;\theta)} {\gamma_{ik}}
       \\ =  &
       \sum\limits_{i=1}^m\sum\limits_{k=1}^K\gamma_{ik}\log \frac {\pi_k\mathcal { N } ( \mathrm { x } | \mu_k , \Sigma_k ) } {\gamma_{ik}}
       \\ =  &
       \sum\limits_{i=1}^m\sum\limits_{k=1}^K\gamma_{ik}\log \frac {\pi_k\frac { 1 } { ( 2 \pi ) ^ { D / 2 }  | \Sigma_k |  ^ { 1 / 2 } } \exp \left[ - \frac { 1 } { 2 } ( x_i - \mu_k ) ^ { T } \Sigma_k  ^ { - 1 } ( x - \mu_k ) \right]} {\gamma_{ik}}
       \\ = & 
        \sum\limits_{i=1}^m\sum\limits_{k=1}^K\gamma_{ik} \log\pi_k
        \\ &- \frac { 1 } { 2 }\sum\limits_{i=1}^m\sum\limits_{k=1}^K \gamma_{ik}  ( x - \mu_k ) ^ { T } \Sigma_k ^ { - 1 } ( x_i - \mu_k ) 
        \\ & + \sum\limits_{i=1}^m\sum\limits_{k=1}^K\gamma_{ik} \log \frac { 1 } { ( 2 \pi ) ^ { D / 2 }  | \Sigma_k |  ^ { 1 / 2 } \gamma_{ik}}   \tag 2
       \end{align}
$$
  由于上面最后一行是常数，在下面求导中，可以忽略。

#### M步

M步将极大化$L(\theta, \theta^{j})$, 得到$\theta^{j+1}$：

接下来，分别对$\pi, \mu, \Sigma$分别求导。首先看$\mu$的导数。
$$
\begin{align}
\frac{\partial L(\theta, \theta^{j})}{\partial \mu_k} 
&= \frac{\partial {-\gamma_{ik} \frac { 1 } { 2 } ( x_i - \mu_k ) ^ { T } \Sigma_k  ^ { - 1 } ( x - \mu_k )}}{\partial \mu_k} 
\\ &= - 
\sum\limits_{i=1}^m\gamma_{ik}  \Sigma_k ^ {-1 }( x_i - \mu_k ) 
\\ &  =
\sum\limits_{i=1}^m\gamma_{ik}  ( \Sigma_k ^ {-1 }x _i - \Sigma_k ^ {-1 }\mu_k  ) 
\end{align}
$$

> 上面用到了向量求导，公式是
> $$
> \frac{\partial \mathbf {w}^\mathbf{T} \mathbf{B} \mathbf {w} } {\partial \mathbf {w} } = 
> \frac {\partial \mathbf {w}^\mathbf{T} } {\partial \mathbf {w} } \cdot \mathbf{B} \mathbf {w} +
> \frac {\partial (\mathbf{B} \mathbf {w})^\mathbf{T} } {\partial \mathbf {w} } \cdot \mathbf {w}=
> (\mathbf{B} + \mathbf{B}^\mathbf{T})\cdot \mathbf {w}
> $$
> 当$\mathbf{B}$是对称矩阵，则$\frac{\partial \mathbf {w}^\mathbf{T} \mathbf{B} \mathbf {w} } {\partial \mathbf {w} } = 2 \mathbf B \mathbf w$，所以得出：
> $$
> \frac{\partial ( x_i - \mu_k ) ^ { T } \Sigma_k ^ { - 1 } ( x_i - \mu_k )}{\partial \mu_k} = 2\Sigma_k ^ { - 1 } ( \mu_k -x_i )
> $$

令$\frac{\partial L(\theta, \theta^{j})}{\partial \mu_k}=0$，则：
$$
\begin{align}
     \sum\limits_{i=1}^m\gamma_{ik}  ( \Sigma_k ^ {-1 }x_i  - \Sigma_k ^ {-1 }\mu_k  ) 
      &= 0
      \\ 
     \Sigma_k ^ {-1 }\sum\limits_{i=1}^m\gamma_{ik}  x_i  - \gamma_{ik}\mu_k   & =0
     \end{align}
$$
由于$\Sigma_k ^ {-1 }$是一个实对称方阵，绝大多数情况其各个向量是线性无关的，所以下面的公式满足。
$$
\begin{align}
 \sum\limits_{i=1}^m\gamma_{ik}  x_i  - \gamma_{ik}\mu_k    &=0
 \\ \mu_k &= \frac {\sum\limits_{i=1}^m\gamma_{ik}  x_i} {\sum\limits_{i=1}^m\gamma_{ik}}
 \end{align}
$$
下面再来看$\pi$的导数。由于$\sum_{k=1}^K \pi_{k} =1$，需要构建[拉格朗日乘数](https://zh.wikipedia.org/zh-hans/%E6%8B%89%E6%A0%BC%E6%9C%97%E6%97%A5%E4%B9%98%E6%95%B0)。即：
$$
R(\pi) = L(\theta, \theta^{j}) + \beta(\sum_{k=1}^K \pi_{k}-1)
$$
令$\frac{\partial R(\pi) }{\partial \pi_k}=0$，则：
$$
\begin{align}
\frac{\partial R(\pi) }{\partial \pi_k} &=0
\\ \frac{\partial  \sum\limits_{i=1}^m\gamma_{ik} \log\pi_k }{\partial \pi_k} + \beta &= 0
\\ \frac {\sum\limits_{i=1}^m\gamma_{ik}} {\pi_k}  + \beta &=0
\\ \pi_k =  \frac {\sum\limits_{i=1}^m\gamma_{ik}} {-\beta}  \tag 2
\end{align}
$$
由于$\sum_{k=1}^K \pi_{k} =1$和$\sum_{k=1}^K \gamma_{ik} = 0$，可得：
$$
\begin{align}
\sum_{k=1}^K  \pi_k &=  \sum_{k=1}^K  \frac {\sum\limits_{i=1}^m\gamma_{ik}} {-\beta}
\\ -\beta &=   \sum\limits_{i=1}^m \sum_{k=1}^K\gamma_{ik}
\\ \beta &= - m
\end{align}
$$
把上面公式带入公式$(2)$，可得：
$$
\pi_k =  \frac 1  {m}  \sum\limits_{i=1}^m\gamma_{ik}
$$

最后再来对$\Sigma$的导数。

这样就完成了一次迭代，然后返回E步进行下一轮迭代。

#### 总结

对上面的流程再进行一下简化，可以得到算法流程如下。

1. 随机初始化模型参数$\theta$的初值$\theta^1= (\pi^1,\mu^1,\Sigma^1)$。

2. for $j$  from $1$ to $J$开始EM算法迭代：

   - E步：
     $$
     \begin{align}
     \gamma_{ik}^j =& \frac{\pi _ { k }^j \mathcal N ( x_i | \mu _ { k }^j , \Sigma _ { k }^j )}
     {\sum _ { l = 1 } ^ { K } \pi_{ l }^j \mathcal N ( x_i | \mu _ { l }^j , \Sigma _ { l } )^j} \\
       L(\theta, \theta^{j}) = & 
             \sum\limits_{i=1}^m\sum\limits_{k=1}^K\gamma_{ik} \log\pi_k
             \\ &- \frac { 1 } { 2 }\sum\limits_{i=1}^m\sum\limits_{k=1}^K \gamma_{ik}  ( x - \mu_k ) ^ { T } \Sigma_k ^ { - 1 } ( x_i - \mu_k ) 
             \\ & + \sum\limits_{i=1}^m\sum\limits_{k=1}^K\gamma_{ik} \log \frac { 1 } { ( 2 \pi ) ^ { D / 2 }  | \Sigma_k |  ^ { 1 / 2 } \gamma_{ik}}   
            \end{align}
     $$
     
   - M步：极大化$L(\theta, \theta^{j})$，$\theta^{j+1}=(\pi^{j+1},\mu^{j+1},\Sigma^{j+1})$，各个参数分别如下：
     $$
     \begin{align}
     \pi_k^{j+1} &=  \frac 1  {m}  \sum\limits_{i=1}^m\gamma_{ik}^j  \\
     \mu_k^{j+1} &= \frac {\sum\limits_{i=1}^m\gamma_{ik}^j  x_i} {\sum\limits_{i=1}^m\gamma_{ik}^j}  \\
     \Sigma _ { k }^{j+1} &= \frac  {\sum _ { i = 1 } ^ { m } \gamma_{ik}^j \left( x _ { i } - \mu _ { k }^j \right) \left( x _ { i } - \mu _ { k }^j \right) ^ { T }} {{\sum\limits_{i=1}^m\gamma_{ik}^j} }
     \end{align}
     $$


## 参考

- [Wiki: K-Means算法](https://zh.wikipedia.org/wiki/K-%E5%B9%B3%E5%9D%87%E7%AE%97%E6%B3%95)

- [K-Means聚类算法原理](https://www.cnblogs.com/pinard/p/6164214.html)

- [EM算法原理及其应用](https://vividfree.github.io/docs/2016-08-19-introduction-about-EM-algorithm-doc1.pdf)

- [EM算法理解的九层境界](https://www.zhihu.com/question/40797593/answer/275171156)

- [K-Means聚类原理](https://zgcr.gitlab.io/2019/03/11/k-means-ju-lei-yuan-li/)

- [详解Kmeans的两大经典优化——mini-batch和Kmeans++](https://juejin.im/post/5e7aa73a5188255e2b57fbbe)

- [EM算法-高斯混合模型GMM](https://www.cnblogs.com/huangyc/p/10125117.html)

- [GMM模型](https://liuyanfeier.github.io/2018/01/04/GMM%E6%A8%A1%E5%9E%8B/)

- [CS229: The EM algorithm](https://see.stanford.edu/materials/aimlcs229/cs229-notes8.pdf)

  







