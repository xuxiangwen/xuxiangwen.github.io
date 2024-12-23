---
title: EM算法实践：抛硬币
categories: algorithm
date: 2020-07-24
---

[EM](https://zh.wikipedia.org/wiki/%E6%9C%80%E5%A4%A7%E6%9C%9F%E6%9C%9B%E7%AE%97%E6%B3%95)（Expectation-Maximum）算法在机器学习中有极为广泛的用途。为了能够加深理解，本文将运用EM算法原理来分析两个抛硬币模型：三硬币模型和两硬币模型。

开始之前，再次复习EM算法的流程。

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

## 三硬币模型

~~~mermaid
graph TD; 
    A((硬币A))--> |pi|B((硬币B));  
    A --> |1-pi|C((硬币C));  
    B --> |p|B1(1);  
    B --> |1-p|B0(0);      
    C --> |q|C1(1);  
    C --> |1-q|C0(0); 

~~~

有三枚硬币A，B，C，先投掷A，如果是正面就投掷B，如果是反面就投掷C，若我们只能观测到最后的投掷结果（B或者C的结果）而不能直到投掷的过程，如何估算三颗硬币的正面率？

### 定义

- 参数$\theta = (\pi,p,q)$，$\pi,p,q$分别是A，B，C三个硬币的正面率。
- 观测到了$m$次投掷结果，记为$x=(x_1,x_2,...x_m)$，$x_i=1$表示正面，$x_i=0$表示反面。
- 隐变量设为$z=(z_1,z_2,...z_m)$，它是硬币A的投掷结果，$z_i=1$表示正面，将选择硬币B，$z_i=0$表示正面，将选择硬币C。

### 算法推导

EM算法过程如下：

1. 随机初始化模型参数$\theta$的初值$\theta^1= (\pi^1,p^1,q^1)$。

2. for $j$  from $1$ to $J$开始EM算法迭代：

   - E步：计算联合分布的条件概率期望：
     $$
     \begin{align}
     Q_i(z_{i}) &= P( z_{i} \vert x_{i};\theta^{j})
     \\ &= \frac {P( z_{i}, x_{i}; \theta^{j})} {P(x_{i}; \theta^{j})}
     \end{align}
     $$
     于是求得：
     $$
     Q_i(z_{i}=1) =
     \frac{\pi^{j}(p^{j})^{x_{i}}(1-p^{j})^{1-x_{i}}}{\pi^{j}(p^{j})^{x_{i}}(1-p^{j})^{1-x_{i}} + (1-\pi^{j})(q^{j})^{x_{i}}(1-q^{j})^{1-x_{i}}}
     $$
     
     记$\mu_i = Q_i(z_{i}=1) $， 由于硬币只有两面，所以$Q_i(z_{i}=0) = 1 - \mu_i  $。下面再来看$L(\theta, \theta^{j})$。
     $$
     \begin{align}
L(\theta, \theta^{j}) &= 
     \sum\limits_{i=1}^m\sum\limits_{z_{i}}Q_i(z_{i})\log \frac {P(x_{i},z_{i};\theta)} {Q_i(z_{i})}
     \\ &=  
     \sum\limits_{i=1}^m 
     \mu_i \log \frac {\pi p^{x_{i}}(1-p)^{1-x_{i}}} {\mu_i} + 
     (1-\mu_i) \log \frac {(1-\pi) q^{x_{i}}(1-q)^{1-x_{i}}} {1-\mu_i} 
     \end{align}
     $$
     
   - M步：极大化$L(\theta, \theta^{j})$, 得到$\theta^{j+1}$：
   
     接下来，分别对$\pi, p, q$分别求导。首先看$\pi$的导数。
     $$
     \begin{align}
     \frac{\partial L(\theta, \theta^{j})}{\partial \pi} &= 
     \sum^{m}_{i=1}u_i\frac{1}{\pi}-(1-u_i)\frac{1}{1-\pi}
     \\&=
     \sum^{m}_{i=1}\frac{u_i-\pi}{\pi(1-\pi)}
     \end{align}
     $$
     令$\frac{\partial L(\theta, \theta^{j})}{\partial \pi}=0$，则：
     $$
     \begin{align}
     \sum^{m}_{i=1}\frac{u_i-\pi}{\pi(1-\pi)} &= 0
     \\ \pi&=\frac{1}{m} \sum_{i=1}^{m} u_{i}
     \end{align}
     $$
     下面再来看$p$的导数。
     $$
     \begin{align}
     \frac{\partial L(\theta, \theta^{j})}{\partial p} &= 
     \sum^{m}_{i=1} \frac{u_ix_i}{p}-\frac{u_i(1-x_i)}{1-p}
     \\&=
     \sum^{m}_{i=1}\frac{\mu_ix_i-\mu_ip}{p(1-p)}
     \end{align}
     $$
     令$\frac{\partial L(\theta, \theta^{j})}{\partial p}=0$，则：
     $$
     \begin{align}
     \sum^{m}_{i=1}\frac{\mu_ix_i-\mu_ip}{p(1-p)} &=0
     \\ p = \frac {\sum^{m}_{i=1}u_ix_i} {\sum^{m}_{i=1} u_i}
     \end{align}
     $$
     最后看$q$的导数，同理，可以得到：
     $$
     q=\frac{\sum^{m}_{i=1}\left(1-u_{i}\right) x_{i}}{\sum^{m}_{i=1}\left(1-u_{i}\right)}
     $$
     然后，设$\theta^{(j+1)} = (\pi, p , q)$，即
     $$
     \theta^{(j+1)} = \left(\pi^{j+1}=\frac 1 m\sum_{i=1}^{m} u_{i}, \ p^{j+1}= \frac {\sum^{m}_{i=1}u_ix_i} {\sum^{m}_{i=1} u_i}, \ q^{j+1}=\frac{\sum^{m}_{i=1}\left(1-u_{i}\right) x_{i}}{\sum^{m}_{i=1}\left(1-u_{i}\right)} \right)
     $$
     这样就完成了一次迭代，返回E步进行下一轮迭代。

对上面的流程再进行一下简化，可以得到算法流程如下。

1. 随机初始化模型参数$\theta$的初值$\theta^1= (\pi^1,p^1,q^1)$。

2. for $j$  from $1$ to $J$开始EM算法迭代：

   - E步：
     $$
     \mu_i =
     \frac{\pi^{j}(p^{j})^{x_{i}}(1-p^{j})^{1-x_{i}}}{\pi^{j}(p^{j})^{x_{i}}(1-p^{j})^{1-x_{i}} + (1-\pi^{j})(q^{j})^{x_{i}}(1-q^{j})^{1-x_{i}}}
     $$

   - M步：得到$\theta^{j+1}$：
     $$
     \theta^{(j+1)} = \left(\pi^{j+1}=\frac 1 m\sum_{i=1}^{m} u_{i}, \ p^{j+1}= \frac {\sum^{m}_{i=1}u_ix_i} {\sum^{m}_{i=1} u_i}, \ q^{j+1}=\frac{\sum^{m}_{i=1}\left(1-u_{i}\right) x_{i}}{\sum^{m}_{i=1}\left(1-u_{i}\right)} \right)
     $$

## 两硬币模型

假设有两枚硬币A、B，以相同的概率随机选择一个硬币，进行如下的掷硬币实验：共做5次实验，每次实验独立的掷10次。当不知道选择的硬币情况下，如何估计两个硬币正面出现的概率？

### 形象理解

下面的图非常形象的描述了整个计算过程。其中，H代表证明正面朝上，T表示反面朝上。

![image-20200724171709033](images/image-20200724171709033.png)

![image-20200724173007865](images/image-20200724173007865.png)

下面我们从EM算法的角度，来推导上面的公式。

### 定义

- 参数$\theta = (\theta_A,\theta_B)$，$\theta_A, \theta_B$分别是A，B两个硬币的正面率。
- 进行了$m$次试验，记为$x=(x_1,x_2,...x_m)$，每次试验，投掷10次，$x_i$表示正面的次数。
- 隐变量设为$z=(z_1,z_2,...z_m)$，它是每次试验选择的硬币，$z_i=A$表示选择硬币A，$z_i=B$表示选择硬币B。

### 算法推导

1. 随机初始化模型参数$\theta$的初值$\theta^1= (\theta_A^1,\theta_B^1)$。

2. for $j$  from $1$ to $J$开始EM算法迭代：

   - E步：计算联合分布的条件概率期望：
     $$
     \begin{align}
     Q_i(z_{i}) &= P( z_{i} \vert x_{i};\theta^{j})
     \\ &= \frac {P( z_{i}, x_{i}; \theta^{j})} {P(x_{i}; \theta^{j})}
     \end{align}
     $$
     于是求得：
     $$
     Q_i(z_{i}=A) =
     \frac
     {(\theta_A^{j})^{x_{i}}(1-\theta_A^{j})^{10-x_{i}}}
     {(\theta_A^{j})^{x_{i}}(1-\theta_A^{j})^{10-x_{i}} + 
      (\theta_B^{j})^{x_{i}}(1-\theta_B^{j})^{10-x_{i}}}
     $$
     
     记$\mu_i = Q_i(z_{i}=A) $，$Q_i(z_{i}=B) = 1 - \mu_i  $。下面再来看$L(\theta, \theta^{j})$
     $$
     \begin{align}
          L(\theta, \theta^{j}) &= \sum\limits_{i=1}^m\sum\limits_{z_{i}}Q_i(z_{i})\log \frac {P(x_{i},z_{i};\theta)} {Q_i(z_{i})}
          \\ &=  \sum\limits_{i=1}^m \mu_i \log \frac {(\theta_A)^{x_{i}}(1-\theta_A)^{10-x_{i}}} {\mu_i} +  (1-\mu_i) \log \frac {(\theta_B)^{x_{i}}(1-\theta_B)^{10-x_{i}}} {1-\mu_i} 
          \end{align}
     $$

  - M步：极大化$L(\theta, \theta^{j})$，得到$\theta^{j+1}$：

     接下来，分别对$\theta_A, \theta_B$分别求导。首先看$\theta_A$的导数。
    $$
    \begin{align}
     \frac{\partial L(\theta, \theta^{j})}{\partial \theta_A} &= 
     \sum^{m}_{i=1}\mu_ix_i\frac{1}{\theta_A}-\mu_i(10-x_i)\frac{1}{1-\theta_A}
     \\&=
     \sum^{m}_{i=1}\frac{\mu_ix_i-10\mu_i\theta_A}{\theta_A(1-\theta_A)}
     \end{align}
    $$
     令$\frac{\partial L(\theta, \theta^{j})}{\partial \theta_A}=0$，则：
    $$
    \begin{align}
     \sum^{m}_{i=1}\frac{\mu_ix_i-10\mu_i\theta_A}{\theta_A(1-\theta_A)} &= 0
     \\ \theta_A&=  \frac {\sum_{i=1}^{m}\mu_{i}x_i} {\sum_{i=1}^{m}10\mu_i}
     \end{align}
    $$
    

    然后看$\theta_B$的导数，同理，可以得到：
    $$
    \theta_B=\frac {\sum_{i=1}^{m}(1-\mu_{i})x_i} {\sum_{i=1}^{m}10(1-\mu_i)}
    $$
    然后，设$\theta^{(j+1)} = (\pi, p , q)$，即
    $$
    \theta^{(j+1)} = \left(\theta_A=  \frac {\sum_{i=1}^{m}\mu_{i}x_i} {\sum_{i=1}^{m}10\mu_i},\  \theta_B=\frac {\sum_{i=1}^{m}(1-\mu_{i})x_i} {\sum_{i=1}^{m}10(1-\mu_i)} \right)
    $$
    这样就完成了一次迭代，返回E步进行下一轮迭代。

对上面的流程再进行一下简化，可以得到算法流程如下。

1. 随机初始化模型参数$\theta$的初值$\theta^1= (\theta_A^1,\theta_B^1)$。

2. for $j$  from $1$ to $J$开始EM算法迭代：

   - E步：
     $$
     \mu_i =
     \frac
     {(\theta_A^{j})^{x_{i}}(1-\theta_A^{j})^{10-x_{i}}}
     {(\theta_A^{j})^{x_{i}}(1-\theta_A^{j})^{10-x_{i}} + 
      (\theta_B^{j})^{x_{i}}(1-\theta_B^{j})^{10-x_{i}}}
     $$
   - M步：得到$\theta^{j+1}$：
     $$
     \theta^{(j+1)} = \left(\theta_A=  \frac {\sum_{i=1}^{m}\mu_{i}x_i} {\sum_{i=1}^{m}10\mu_i},\  \theta_B=\frac {\sum_{i=1}^{m}(1-\mu_{i})x_i} {\sum_{i=1}^{m}10(1-\mu_i)} \right)
     $$

通俗起来可以这么理解，E步计算每一次试验选择A的概率。M步中，分母$\sum_{i=1}^{m}10\mu_i$理解为，把多少试验次数分配到A，而分子$\sum_{i=1}^{m}\mu_{i}x_i$理解为，把多少次正面次数分配到A。

### 代码实现

下面是相关代码实现。

~~~python
import numpy as np

def coin_probability(coin_toss, p):
    p_coin = np.zeros((coin_toss.shape[0], len(p)))
    for i, toss in enumerate(coin_toss):
        p_toss = np.array([ np.array([prob, 1-prob])[1-toss] for prob in p ])
        p_coin[i] = np.prod(p_toss, axis=1)   
    p_coin = p_coin/np.sum(p_coin, axis=1, keepdims=True)
    return p_coin

def simple_em(coin_toss, p, epochs=10):

    next_p = p
    print('{} epoch: {}'.format(0, next_p)) 
    for epoch in range(epochs):
        p_coin = coin_probability(coin_toss, next_p)        
        next_p = np.sum(coin_toss, axis=1).dot(p_coin)/(np.sum(p_coin, axis=0)*coin_toss.shape[1])
        print('{} epoch: {}'.format(epoch+1, next_p))   
            
    p_coin = coin_probability(coin_toss, next_p)  
    coins = np.argmax(p_coin, axis=1)
    return next_p, coins


#1 代表抛到正面，0表示反面
coin_toss = np.array([[1, 0, 0, 0, 1, 1, 0, 1, 0, 1],
                      [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
                      [1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
                      [1, 0, 1, 0, 0, 0, 1, 1, 0, 0],
                      [0, 1, 1, 1, 0, 1, 1, 1, 0, 1]])

p = np.array([0.6, 0.5])
new_p, coins = simple_em(coin_toss, p, 20)  
~~~

![image-20200724201803116](images/image-20200724201803116.png)

即使初始的概率值不相同，也会收敛到相同的参数。

~~~python
p = np.array([0.8, 0.2])
simple_em(coin_toss, p, 20)  
~~~

![image-20200724201838171](images/image-20200724201838171.png)

## 参考

- [EM算法推导与三硬币模型](https://galaxychen.github.io/2019/07/22/em-and-three-coins/)
- [EM算法原理及其应用](https://vividfree.github.io/docs/2016-08-19-introduction-about-EM-algorithm-doc1.pdf)
- [EM算法实例分析](https://chenrudan.github.io/blog/2015/12/02/emexample.html)
- [What is the expectation maximization
  algorithm?](http://ai.stanford.edu/~chuongdo/papers/em_tutorial.pdf)

