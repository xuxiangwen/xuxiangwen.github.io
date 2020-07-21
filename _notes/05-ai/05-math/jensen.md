---
title: Jensen不等式
categories: mathematics
date: 2020-07-14
---

Jensen不等式（Jensen's inequality），以丹麦数学家Johan Jensen命名，它给出积分的凸函数值和凸函数的积分值间的关系，它在概率论、机器学习、测度论、统计物理等领域都有相关应用。

## 定义

对于任意点集${x_i}$，若$\lambda_i \geq 0 $，且$\sum_{i=1}^{M} \lambda_{i}=1$，则凸函数$f(x)$满足下面的公式。
$$
f\left(\sum_{i=1}^{M} \lambda_{i} x_{i}\right) \leq \sum_{i=1}^{M} \lambda_{i} f\left(x_{i}\right)
$$
在概率论中，如果把 $\lambda_i$ 看成概率分布，那么公式就可以写成：
$$
f(E[x]) \leq E[f(x)]
$$

反之，如果$f(x)$是凹函数，则：
$$
f\left(\sum_{i=1}^{M} \lambda_{i} x_{i}\right) \geq \sum_{i=1}^{M} \lambda_{i} f\left(x_{i}\right) \\
f(E[x]) \geq E[f(x)]
$$

## 证明

首先我们来看当$M=2$的情况，即
$$
f\left(tx_1+(1-t)x_2\right) \leq tf(x_1)+(1-t)f(x_2) 
$$
如下图所示，当$f(x)$时凸函数（二阶导数大于等于0），上面的公式显然成立。

![img](https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/ConvexFunction.svg/400px-ConvexFunction.svg.png)

下面我们来看当$M>2$的情况。
$$
f\left(\sum_{i=1}^{M} \lambda_{i} x_{i}\right) \leq \sum_{i=1}^{M} \lambda_{i} f\left(x_{i}\right)
$$
假设上面的公式成立，下面我们来证明$M+1$的情况下，公式依然成立，即
$$
f\left(\sum_{i=1}^{M+1} \lambda_{i} x_{i}\right) \leq \sum_{i=1}^{M+1} \lambda_{i} f\left(x_{i}\right)   \tag 1
$$
首先把$M+1$个数分成两部分，即
$$
\begin{align}
\sum_{i=1}^{M+1} \lambda_{i} x_{i} 
& = 
\lambda_1x_1 + \sum_{i=2}^{M} \lambda_{i} x_{i}
\\ & = 
\lambda_1x_1 + (1-\lambda_1) \sum_{i=2}^{M+1} \frac {\lambda_{i} } {1-\lambda_1}x_{i}
\end{align}
$$
设$x^*=\sum_{i=2}^{M+1} \frac {\lambda_{i}} {1-\lambda_1}  x_{i}$，则：
$$
\begin{align}
f\left(\sum_{i=1}^{M+1} \lambda_{i} x_{i}\right) = f(\lambda_1x_1+(1-\lambda_1)x^*)
\end{align}
$$
然后根据公式$f\left(tx_1+(1-t)x_2\right) \leq tf(x_1)+(1-t)f(x_2) $，则：
$$
\begin{align}
f\left(\sum_{i=1}^{M+1} \lambda_{i} x_{i}\right) 
&= f(\lambda_1x_1+(1-\lambda_1)x^*)
\\ & \leq
\lambda_1f(x_1) + (1-\lambda_1)f(x^*)
\\ & = 
\lambda_1f(x_1) + (1-\lambda_1)f\left(\sum_{i=2}^{M+1} \frac {\lambda_{i} } {1-\lambda_1} x_{i} \right)  \tag 2
\end{align}
$$
由于$\sum_{i=2}^{M+1} \frac {\lambda_{i} x_{i}} {1-\lambda_1}$刚好是$M$个数相加，根据公式$(1)$，可以得到：
$$
f\left(\sum_{i=2}^{M+1} \frac {\lambda_{i} } {1-\lambda_1} x_{i} \right) \leq \sum_{i=2}^{M+1} \frac {\lambda_{i} } {1-\lambda_1} f\left(x_{i}\right)
$$
把上面公式带入公式$(2)$，可以得到：
$$
\begin{align}
f\left(\sum_{i=1}^{M+1} \lambda_{i} x_{i}\right) 
& \leq
\lambda_1f(x_1) + (1-\lambda_1)f\left(\sum_{i=2}^{M+1} \frac {\lambda_{i} } {1-\lambda_1} x_{i} \right)  
\\ & \leq 
\lambda_1f(x_1) + (1-\lambda_1)\sum_{i=2}^{M+1} \frac {\lambda_{i} } {1-\lambda_1} f\left(x_{i}\right)
\\ & =
\sum_{i=1}^{M+1} \lambda_if(x_i)
\end{align}
$$
证毕。

## 参考

- [Jensen's inequality](https://en.wikipedia.org/wiki/Jensen's_inequality)