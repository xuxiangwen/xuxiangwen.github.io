
# 逻辑回归 （Logistic Regression）

$ h(x)= \frac {1} {1+e^{-x}}$

$ h(-x) + h(x) = 1$

$ \frac{\mathrm{d}h(x)^\mathrm{T}} {\mathrm{d}x} = diag(h(x)*(1-h(x))) =  diag(h(x)*h(-x))$ 

$ \frac{\mathrm{d}h(Xw)^\mathrm{T}} {\mathrm{d}w} = 
X^\mathrm{T} \cdot diag(h(Xw)*(1-h(Xw))) 
$ 

$ \frac{\mathrm{d}(1-h(Xw))^\mathrm{T}} {\mathrm{d}w} = 
-X^\mathrm{T} \cdot diag(h(Xw)*(1-h(Xw))) 
$ 

$ \frac{\mathrm{d}log(h(Xw))^\mathrm{T}} {\mathrm{d}w} = 
X^\mathrm{T} \cdot diag(h(Xw)*(1-h(Xw))) \cdot diag(1/h(Xw)) =
X^\mathrm{T} \cdot diag(1-h(Xw))
$ 

$ \frac{\mathrm{d}log(1-h(Xw))^\mathrm{T}} {\mathrm{d}w} = 
-X^\mathrm{T} \cdot diag(h(Xw)*(1-h(Xw))) \cdot diag(1/(1-h(Xw))) =
-X^\mathrm{T} \cdot diag(h(Xw))
$ 

## 1. 方式一
设  $y \in \{0， 1\}$

### cost函数

$L(w) = -\frac 1 m  {\log (h(Xw))}^\mathrm{T}y - \frac 1 m{\log (1-h(Xw))}^\mathrm{T}(1-y) + \frac \lambda {2m}\lVert {w} \rVert _{2} $

### 梯度

设$z = Xw$, 不考虑正则项，可以推出以下公式

$\nabla{z} =   - \frac 1 m \frac{\mathrm{d}log(h(z))^\mathrm{T}} {\mathrm{d}z}  \cdot y  - \frac 1 m  \frac{\mathrm{d}log(1-h(z))^\mathrm{T}} {\mathrm{d}z} \cdot（1-y）
$

$\nabla{z} =  - \frac 1 m  diag(1-h(z))\cdot y + 
\frac 1 m diag(h(z)) \cdot（1-y）$

$\nabla{z} = \frac 1 m  (h(Xw) - y) $

上面公式非常简洁。下面是完整的。

$\nabla{w} =   - \frac 1 m \frac{\mathrm{d}log(h(Xw))^\mathrm{T}} {\mathrm{d}w}  \cdot y  - \frac 1 m  \frac{\mathrm{d}log(1-h(Xw))^\mathrm{T}} {\mathrm{d}w} \cdot（1-y）+ \frac \lambda m w
$

$\nabla{w} =  - \frac 1 m X^\mathrm{T} \cdot diag(1-h(Xw))\cdot y + 
\frac 1 m X^\mathrm{T} \cdot diag(h(Xw)) \cdot（1-y）+ \frac \lambda m w$

$\nabla{w} = \frac 1 m X^\mathrm{T} \cdot (h(Xw) - y) + \frac \lambda m w$


## 2. 方式二

设  $y \in \{-1， 1\}$

### cost函数

根据最大似然估计的假设

$P(w) = {\prod \limits_i  }h(x_i^\mathrm{T}w)|_{y=1}* \prod \limits_i (1-h(x_i^\mathrm{T}w))|_{y=-1} $

$P(w) = {\prod \limits_i  }h(x_i^\mathrm{T}w)|_{y=1}* \prod \limits_i h(-x_i^\mathrm{T}w))|_{y=-1}  $

$P(w) = \prod \limits_i  h(y_i x_i^\mathrm{T}w) $

$L(w) = -\frac 1 m \sum\limits_i^m log(P(w)) + \frac \lambda {2m}\lVert {w} \rVert _{2}$

$L(w) = -\frac 1 m \sum\limits_i^m log(h(y_ix_i^\mathrm{T}w) )  + \frac \lambda {2m}\lVert {w} \rVert _{2}  $

$L(w) = -\frac 1 m \sum log(h(y *  Xw)) + \frac \lambda {2m}\lVert {w} \rVert _{2}$

$L(w) = -\frac 1 m \sum log(h(diag(y)\cdot Xw))+ \frac \lambda {2m}\lVert {w} \rVert _{2}  $

$L(w) = -\frac 1 m \sum log(h(y * Xw))+ \frac \lambda {2m}\lVert {w} \rVert _{2} $

### 梯度

$\nabla{w} = -\frac 1 m \sum\limits_i^m   \frac {\mathrm{d}log(h(y_ix_i^\mathrm{T}w))} {\mathrm{d}w}  + \frac \lambda m w$

$\nabla{w} = -\frac 1 m \sum\limits_i^m   y_ix_i(1-h(y_ix_i^\mathrm{T}w)) + \frac \lambda m w $

$\nabla{w} = -\frac 1 m X^\mathrm{T} \cdot diag(y) \cdot (1-h(diag(y) \cdot Xw)) + \frac \lambda m w $

$\nabla{w} = -\frac 1 m X^\mathrm{T} \cdot  (y*(1-h(y*Xw))) + \frac \lambda m w $

### 理解

可以把激活函数返回的结果看成是，y=1发生的概率

$ p_{y=1} = h(x)= \frac {1} {1+e^{-x}}   \\ 
p_{y=0} = h(x)= \frac {e^{-x}} {1+e^{-x}}  \\
\frac {p_{y=1}} {p_{y=0} } = e^{x} \\
\log {\frac {p_{y=1}} {p_{y=0} }} = x
$


这里加入一些对$e, e^x$的理解。我们都知道

$e = \lim\limits_{n\to\infty}(1+ \frac 1 n)^n$

$e^x = \lim\limits_{n\to\infty}(1+ \frac x n)^n$

对于$e^x$是一种复利的计算方式，是否也可以代表一种能量方式呢。物质无限可分，我们关心的事件，或许也是由某种规律的重复而再现的。

##  参见 
1. [数学里的 e 为什么叫做自然底数？是不是自然界里什么东西恰好是 e？](https://www.zhihu.com/question/20296247)
2. [e (数学常数)](https://zh.wikipedia.org/wiki/E_(%E6%95%B0%E5%AD%A6%E5%B8%B8%E6%95%B0))
3. [数学常数e的含义](http://www.ruanyifeng.com/blog/2011/07/mathematical_constant_e.html)


```python

```


```python

```


```python

```
