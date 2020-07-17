---
title: 马尔科夫链-蒙特卡洛方法
categories: statistics
date: 2020-07-04
---

马尔科夫链-蒙特卡洛方法（Markov Chain Monte Carlo ）简称MCMC。显然，从名字上可以看出，这个方法包括：马尔可夫链和蒙特卡洛方法，下面我们一一道来。

## 预备知识

下面来梳理以下其中的关系

-  [马尔科夫链](markov_chain.md) 

- [蒙特卡罗方法](monte_carlo.md) 

  蒙特卡罗的核心思想是通过大量随机样本，来获取对系统的估计，取样越多，估计越准确。通过计算机中，可以快速模拟大量的抽样，这使得蒙特卡罗思想运用的越来越广泛。蒙特卡罗方法的核心问题是就，如何准确并且快速的取样。下面是一些取样方法。

  -  [逆变换采样](inverse_transform_sampling.md) 

    如果知道一个分布的累积分布函数，及其反函数，可以用逆变换采样的方法来获取样本。

  - [Box-Muller变换](box-muller.md) 

    运用逆变换采样的原理来获取正态分布的样本。具体来说，是通过服从均匀分布的随机变量，来构建服从高斯分布的样本。

  - [拒绝采样](rejection_sampling.md) 

    逆变换采样必须知道 CDF 及其 反函数，很多情况下是无法实现的。如果只知道概率密度函数（PDF），可以使用拒绝采样的方法来获取样本。

    拒绝分布的难点在于是否能找到一个合适的$M q(x)$，因为这个函数需要能够覆盖$p(x)$。

  - [重要性采样](importance_sampling.md) 

    重要性

  -  [Gibbs采样](gibbs_sampling.md) 



## 

## MCMC采样

由于一般情况下，目标平稳分布$\pi(x)$和某一个状态转移矩阵$Q$不满足细致平稳条件，即
$$
\pi(i)P(i,j) \neq \pi(j)P(j,i)
$$

> 这里有个疑问，为啥自己随机生成的例子中，都是平稳的，但不符合上面公式。

我们可以对上式做一个改造，使细致平稳条件成立。方法是引入一个$\alpha(i, j)$,使上式可以取等号，即：
$$
\pi(i)Q(i,j)\alpha(i,j) = \pi(j)Q(j,i)\alpha(j,i)
$$
当满足下两式，上面等式就自然成立：
$$
\alpha(i,j) = \pi(j)Q(j,i) \\
\alpha(j,i) = \pi(i)Q(i,j)
$$
这样我们就得到了新的状态转移矩阵。可以用下面的图示，来理解这一过程。





## 参考

- [MCMC(二)马尔科夫链](https://www.cnblogs.com/pinard/p/6632399.html)
- [从随机过程到马尔科夫链-蒙特卡洛方法](https://github.com/dailiang/cnblogs/blob/master/MCMC/MCMC.md)