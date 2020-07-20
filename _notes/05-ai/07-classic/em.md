---
title: LDA详解
categories: statistics
date: 2020-07-23
---

## 预备知识

### Jensen 不等式

Jensen不等式（Jensen's inequality）是以丹麦数学家Johan Jensen命名的，它在概率论、机器学习、测度论、统计物理等领域都有相关应用。其定义如下：

对于任意点集${x_i}$，若$\lambda_i \geq 0 $，且$\sum_{i=1}^{M} \lambda_{i}=1$，则凸函数$f(x)$满足下面的公式。
$$
f\left(\sum_{i=1}^{M} \lambda_{i} x_{i}\right) \geq \sum_{i=1}^{M} \lambda_{i} f\left(x_{i}\right)
$$
**在概率论中**，如果把 $\lambda_i$ 看成概率分布，那么公式就可以写成：
$$
f(E[x]) \geq E[f(x)]
$$

## EM算法推导

首先考虑最一般化的极大似然，我们在获得观测变量$Y$时，希望最大化$Y$出现的概率，即极大化目标函数。
$$
L(\theta)=\log P(Y | \theta)=\log \sum_{Z} P(Y, Z | \theta)=\log \left(\sum_{Z} P(Y | Z, \theta) P(Z | \theta)\right)
$$
其中，$\theta$是模型的参数，$Z$是隐变量。上面使用到了全概率公式和条件概率公式。接下来使用迭代的方式逐步更新$\theta$的值，试图在迭代的过程中增大$L(\theta)$的值。那么如何更新$\theta$呢？假设我们现在已经进行了$i$轮的迭代，当前的模型参数为$\theta^{(i)}$，我们来考虑一下迭代后的目标函数$L(\theta)$和迭代前的目标函数$L(\theta^i)$的差值（注$L(\theta^{(i)})$是指使用当前模型的参数计算出来的目标函数值）。
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


## 参考

- [Jensen's inequality](https://en.wikipedia.org/wiki/Jensen's_inequality)
- [EM算法推导与三硬币模型](https://galaxychen.github.io/2019/07/22/em-and-three-coins/)