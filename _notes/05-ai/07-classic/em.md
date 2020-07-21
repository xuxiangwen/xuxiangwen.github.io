---
title: EM算法
categories: statistics
date: 2020-07-23
---

EM（Expectation-Maximum）算法也称期望最大化算法，它是1977年由Dempster等人总结 提出。EM算法是最常见的隐变量估计方法，在机器学习中有极为广泛的用途，例如常被用来学习高斯混合模型（Gaussian Mixture Model，简称GMM）的参数；隐式马尔科夫算法（HMM）、LDA主题模型的变分推断等等。

EM算法是一种迭代优化策略，由于它的计算方法中每一次迭代都分两步，其中一个为期望步（**E**xpectation步），另一个为极大步（**M**aximum步），故此得名。

## 问题描述

在构建模型时，我们需要从样本观察数据中，找出样本的模型参数。 而最常用的方法就是极大对数似然估计。 定义如下：

对于$m$个样本观察数据$x=(x_1,x_2,...x_m)$中，找出样本的模型参数$\theta$，采用最大对数似然估计如下：
$$
L(\theta) = \sum\limits_{i=1}^m logP(x_i;\theta)
$$
通过极大化$L(\theta)$，来获得对应的模型参数$\theta$。

然而，在很多情况下，有隐藏变量决定观测数据，则函数变成：
$$
L(\theta) = \sum\limits_{i=1}^m log\sum\limits_{z_i}P(x_i, z_i;\theta) \tag 1
$$
其中隐藏变量$z=(z_1. z_2,...,z_m)$。下面我们来逐步分析，EM算法如何来根据隐藏变量$z$求解$\theta$。

## 算法推导

EM算法的基本思路是，找到最大似然估计的一个下界，然后不停的迭代，每一次迭代保证的值会逐步提高，这样就会慢慢接近最大似然估计的（局部）最大值，然后获得其对应的模型参数$\theta$。

### 函数的下界

首先我们来看看，最大似然估计的下界。由于log函数是一个凹函数，根据Jensen 不等式，可以得到。
$$
\begin{align}
L(\theta) &= \sum\limits_{i=1}^m log \sum\limits_{z_i}P(x_i, z_i;\theta)
\\ &
=  \sum\limits_{i=1}^m log\sum\limits_{z_i}Q_i(z_i)\frac{P(x_i， z_i;\theta)}{Q_i(z_i)} 
\\ & 
\geq \sum\limits_{i=1}^m  \sum\limits_{z_i} Q_i(z_i)log\frac{P(x_i， z_i;\theta)}{Q_i(z_i)} 
\end{align}
$$
其中$Q_i(z_i)$是对于$z_i$的概率分布。

### 迭代的收敛性





根据
$$
L(\theta)=\log P(Y | \theta)=
$$

$$
L(\theta)=\log P(Y | \theta)=\log \sum_{Z} P(Y, Z | \theta)=\log \left(\sum_{Z} P(Y | Z, \theta) P(Z | \theta)\right)
$$
其中，$\theta$是模型的参数，$Z$是隐变量。接下来使用迭代的方式逐步更新$\theta$的值，试图在迭代的过程中增大$L(\theta)$的值。那么如何更新$\theta$呢？假设我们现在已经进行了$t$轮的迭代，当前的模型参数为$\theta^{(t)}$，我们来考虑一下迭代后的目标函数$L(\theta)$和迭代前的目标函数$L(\theta^i)$的差值（注$L(\theta^{(i)})$是指使用当前模型的参数计算出来的目标函数值）。
$$
\begin{align}
L(\theta)-L\left(\theta^{(i)}\right)
& = \log P(Y | \theta) - \log P\left(Y | \theta^{(i)}\right)
\\ &=\log \left(\sum_{Z} P(Y | Z, \theta) P(Z | \theta)\right)-\log P\left(Y | \theta^{(i)}\right)
\\ &=\log \left(\sum_{Z} P\left(Z | Y, \theta^{(i)}\right) \frac{P(Y | Z, \theta) P(Z | \theta)}{P\left(Z | Y, \theta^{(i)}\right)}\right)-\log P\left(Y | \theta^{(i)}\right)
\end{align}
$$

然后根据Jensen 不等式，替换上式中的左边部分，可以得到：
$$
\begin{align}
L(\theta)-L\left(\theta^{(i)}\right)
 & \geqslant
 \sum_{Z} P\left(Z | Y, \theta^{(i)}\right) \log \frac{P(Y | Z, \theta) P(Z | \theta)}{P\left(Z | Y, \theta^{(i)}\right)}-\log P\left(Y | \theta^{(i)}\right)
 \end{align}
$$
由于$\sum_{Z} P\left(Z | Y, \theta^{(i)}\right)=1$，且$\log P\left(Y | \theta^{(i)}\right)$中不包含$Z$，替换上式中的右边部分，可以得到：
$$
\begin{align}
L(\theta)-L\left(\theta^{(i)}\right)
&  \geq \sum_{Z} P\left(Z | Y, \theta^{(i)}\right) \log \frac{P(Y | Z, \theta) P(Z | \theta)}{P\left(Z | Y, \theta^{(i)}\right)}-\sum_{Z} P\left(Z | Y, \theta^{(i)}\right)\log P\left(Y | \theta^{(i)}\right)
\\ & =
\sum_{Z} P\left(Z | Y, \theta^{(i)}\right) \left[\log \frac{P(Y | Z, \theta) P(Z | \theta)}{P\left(Z | Y, \theta^{(i)}\right)}- \log P\left(Y | \theta^{(i)}\right)\right]
\\ & =
\sum_{Z} P\left(Z | Y, \theta^{(i)}\right) \log \frac{P(Y | Z, \theta) P(Z | \theta)}{P\left(Z | Y, \theta^{(i)}\right) P\left(Y | \theta^{(i)}\right)}
\end{align}
$$



## 三硬币模型



## GMM算法





## 参考

- [最大期望算法](https://zh.wikipedia.org/wiki/%E6%9C%80%E5%A4%A7%E6%9C%9F%E6%9C%9B%E7%AE%97%E6%B3%95)
- [EM算法详解](https://zhuanlan.zhihu.com/p/40991784)
- [EM算法原理总结](https://www.cnblogs.com/pinard/p/6912636.html)
- [EM算法推导与三硬币模型](https://galaxychen.github.io/2019/07/22/em-and-three-coins/)
- [EM算法原理及其应用](https://vividfree.github.io/docs/2016-08-19-introduction-about-EM-algorithm-doc1.pdf)

