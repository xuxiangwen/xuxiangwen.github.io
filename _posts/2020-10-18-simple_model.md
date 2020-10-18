---
# generated from _notes/05-ai/10-base/simple_model.md

title: 几个基本模型
categories: linear-algebra
date: 2020-10-18
---

本文主要汇总一些基本且常用的算法和模型，简述原理，并做必要公式推导，用于备忘，而且不定期更新中。

## 1. 线性回归

线性回归（Linear Regression）是利用称为线性回归方程的最小二乘函数对一个或多个自变量和因变量之间关系进行建模的一种回归分析. 

![Gradient descent for linear regression using Golang](/assets/images/Nulab-Gradient-descent-for-linear-regression-using-Golang-Blog.png)

### 1.1 模型

设$X \in R^{m \times n}, w \in R^{n\times 1}, \hat y,y \in  R^{m \times 1} $，$\hat y $是模型的预测值。

$$

\hat y = Xw

$$

### 1.2 策略

损失函数定义如下，需要最小化该函数。y

$$

\begin{align}
J(w) &= \frac 1 {2m}  \sum_{i=1}^m (\hat y_i - y_i)^2    \\
     &= \frac 1 {2m} (\hat  y - y)^\mathrm{T}( \hat  y  - y)      \\
     &= \frac 1 {2m} (Xw - y)^\mathrm{T}(Xw - y)     
\end{align}

$$

### 1.3 算法

#### 1.31方程

$$

w = {(X^\mathrm{T}X)^{-1}}X^\mathrm{T}y

$$

##### 投影

![](/assets/images/projection.jpg)

可以把$\hat y$ 看成是$y$ 在$X$向量空间的投影, 而$w$看成$\hat y$在$X$的坐标.  所以$ \hat y  - y $得到的向量应该和$X$垂直. 也就是满足如下公式.

$$

\begin{align}
X^T (\hat y - y) = 0  \\
X^T (Xw - y) = 0  \\ 
w = {(X^\mathrm{T}X)^{-1}}X^\mathrm{T}y  
\end{align}

$$

##### 梯度极值法

$$

\begin{align}
	J(w) &= (Xw-y)^T(Xw-y) \\ 
		 &= (w^TX^T-y^T)(Xw-y) \\ 
		 &= w^TX^TXw - w^TX^Ty - y^TXw + y^Ty \\
		 &= w^TX^TXw - y^TXw - y^TXw + y^Ty \\
		 &= w^TX^TXw - 2y^TXw + y^Ty \\
\end{align}

$$

$J(w)$是个凸函数，最小值在所有偏导为0的地方，

$$

\begin{align}
& \frac{\partial J(w)}{\partial w} = 2X^TXw - 2X^Ty = 0 \\
& w = {(X^\mathrm{T}X)^{-1}}X^\mathrm{T}y  
\end{align}

$$

#### 1.32 梯度下降

$$

\nabla{w} = \frac 1 m X^\mathrm{T}(Xw - y)

$$

推导如下：

$$

\begin{align}
\nabla{w} &= \frac {\partial J(w)} {\partial w} 
\\ &=    \frac {\partial (Xw-y)^T}  {\partial w} \frac {\partial \frac 1 {2m} (Xw - y)^\mathrm{T}(Xw - y)} {\partial (Xw-y)} 
\\ &=   X^T \frac 1 {2m} 2(Xw - y)
\\ &=  \frac 1 {m}X^T(Xw - y)
\end{align}

$$

上面推导主要调用了以下两个公式。

$$

\frac{\partial \mathbf {w}^\mathbf{T}\mathbf {w} }{\partial \mathbf {w} } = 2\mathbf {w} \\
\frac{\partial (\mathbf{A}\mathbf {w})^\mathbf{T} }{\partial \mathbf {w} } = = 
\mathbf{A}^\mathbf{T}

$$

## 2. 逻辑回归 

逻辑回归（Logistic Regression）是一种线性模型，用于二分类，运用非常广泛。

![image-20201015152715767](/assets/images/image-20201015152715767.png)

### 2.1 模型

![img](/assets/images/sigmoid.gif)

设$X \in R^{m \times n}, w \in R^{n\times 1}, z,h(z),y \in  R^{m \times 1} $，采用sigmoid函数。

$$

h(z) = \frac{1}{1+e^{-z}}

$$

其中$ z = Xw$。

很明显，对于某一个样本$x_i$（是一个行向量），$z_i=x_iw$。$h(z_i)$表示该样本属于第一个类别的概率，$1-h(z_i)$表示该样本属于第二个类别的概率。

### 2.2 策略

损失函数采用交叉熵来定义。

$$

J(w) = \frac 1 m \left(-y^T\log h(z) - (1-y)^T \log (1-h(z))\right)

$$

该函数来自对数极大似然函数，其关键如下。

- 对于单个样本$x_i$，其发生的概率是$h(z_i)^{y_i}(1-h(z_i))^{1-y_i}$

  这个公式挺巧妙的，无论样本是属于第一个类别，还是第二个类别，都能够表示样本发生的概率。

- 对上步的公式，取log，然后取负号，便可以得到损失函数。

  $$

  -y_i\log h(z_i) -  (1-y_i) \log(1-h(z_i))

  $$

### 2.3 算法

采用梯度下降求解参数。

$$

\nabla{w} = \frac 1 m X^\mathrm{T}(h(z) - y)

$$

推导如下。

$$

\begin{align}
\nabla{w} &= \frac {\partial J(w)} {\partial w} 
\\ &=  - \underbrace{\frac {\partial { \frac 1 m  y^T\log h(z)}}  {\partial w}}_{(a)} - \underbrace{\frac {\partial { \frac 1 m  (1-y)^T \log (1-h(z))}}  {\partial w}}_{(b)} 
\end{align} \tag 1

$$

下面来推导上面的$(a)$和$(b)$。首先来看$(a)$。

$$

\begin{align}
\frac {\partial {\frac 1 m  y^T\log h(z)}}  {\partial w} &= 
\frac {\partial z^T} {\partial w} 
\cdot\frac {\partial h(z)^T} {\partial z} 
\cdot\frac {\partial {\log h(z)^T}} {\partial h(z)} 
\cdot\frac {\partial {\frac 1 m  y^T\log h(z)}} {\partial \log h(z)}
\\ &=  X^T \circ  \left ( h(z)^T  (1-h(z))^T \right )  \circ  \frac 1 {h(z)^T} \cdot \frac 1 m y 
\\ &= \frac 1 m X^T \cdot  (1-h(z))y  
\\ &= \frac 1 m X^T (y-h(z)y) 
\end{align}

$$

同理可以计算$(b)$。

$$

\begin{align}
\frac {\partial { \frac 1 m  (1-y)^T \log (1-h(z))}}  {\partial w} &= 
\frac {\partial z^T} {\partial w} 
\cdot\frac {\partial (1-h(z))^T} {\partial z} 
\cdot\frac {\partial {\log (1-h(z))^T}} {\partial (1-h(z))} 
\cdot\frac {\partial {\frac 1 m  (1-y)^T \log (1-h(z))}} {\partial \log (1-h(z))}
\\ &=  X^T \circ  \left (-h(z)^T (1-h(z))^T  \right ) \circ  \frac 1 {(1-h(z))^T}  \cdot  \frac 1 m (1-y )
\\ &= \frac 1 m X^T \cdot h(z) (y-1)
\\ &= \frac 1 m X^T \cdot  (h(z)y-h(z))
\end{align}

$$

把$(a)$和$(b)$带入公式$(1)$，推导完成。

$$

\begin{align}
\nabla{w} &= - \frac 1 m X^T \cdot (y-h(z)y)  - \frac 1 m X^T \cdot  (h(z)y-h(z))
 \\ &=  \frac 1 m X^T (h(z) -y)
\end{align}

$$

不难发现，Logistic Regression其梯度求解和线性回归的结构完全相同。

上面推导主要用到了sigmoid函数和log函数的求导，详见[sigmoid函数导数](https://eipi10.cn/linear-algebra/2019/12/12/common_vector_derivative/#sigmoid%E5%87%BD%E6%95%B0)。

## 3. Softmax回归

Softmax回归（Softmax Regression）也是一种线性模型，它是逻辑回归的推广，用于多分类。

### 3.1 模型

![image-20201015162945377](/assets/images/image-20201015162945377.png)

上图中$ x $表示一个样本，$ z = Wx$，且

$$

W = \begin{bmatrix} w_1^T \\ w_2^T \\ \vdots \\ w_K^T \end{bmatrix} ，
z = \begin{bmatrix} z_1 \\ z_2 \\ \vdots \\ z_K \end{bmatrix}= \begin{bmatrix} w_1^Tx \\ w_2^Tx \\ \vdots \\ w_K^Tx \end{bmatrix}

$$

$$

\begin{align}
a_i = h(z_i) =   \frac {e^{z_i}}  {\sum_{k=1}^K e^{z_k}}
\end{align}

$$

采用向量的表示如下：

$$

\begin{align}
a = h(z) =   \frac {e^z}  {d^T \cdot e^z}
\end{align}

$$

其中$ d^T = \begin{bmatrix} 1 & 1& \cdots 1 \end{bmatrix}$。

扩展到m个样本，设设$X \in R^{n \times m}, w \in R^{k \times n}, Z, A, Y \in  R^{k \times m},Z = W \cdot X $，则：

$$

\begin{align}
A = h(Z) =   \frac {e^Z}  {d^T \cdot e^Z}
\end{align}

$$

### 3.2 策略

单样本的损失函数如下：

$$

j = - \log a^T y

$$

m个样本的损失函数定义如下。

$$

\begin{align}
J(W) = -  \frac 1 m \sum \log A \circ Y 
\end{align}

$$

### 3.3 算法

采用梯度下降求解参数。分成两步。

#### 对$Z$的偏导数

首先看单样本。

$$

\begin{align}
 \frac {\partial j} {\partial z}  &=  
\frac {\partial a^T} {\partial z} 
\cdot\frac {\partial {\log a^T}} {\partial a} 
\cdot\frac {\partial {-  \log a^{T} \cdot y }} {\partial \log a}
\\ &=   \left ( diag(a) - a \cdot {a}^{T} \right ) \circ \frac 1 {a^T} \cdot (- y)
\\ &=  \left ( a \cdot d^T -1 \right )  \cdot y   
\\ &=    a \cdot d^T \cdot y  - y   & 由于d^T \cdot y = 1
\\ &=    a  - y   
\end{align}

$$

很容易，推广到所有样本，则：

$$

\begin{align}
\frac {\partial {J(W)}} {\partial Z} 
&=  \frac 1 m (A - Y)
\end{align}

$$

#### 对$W$的偏导数

$$

W = \begin{bmatrix} w_1^T \\ w_2^T \\ \vdots \\ w_K^T \end{bmatrix}

$$

为了简化，首先计算对$W$中某一行（记为$w$）的偏导数，满足$z^T = w^T X$，推导如下：

$$

\begin{align}
\frac {\partial J(W)} {\partial w}  &=  
\frac {\partial z^T} {\partial w} \cdot \frac {\partial J(W)} {\partial z}  
\\ &=   X \cdot \frac 1 m (a-y)^T 
\\ &=  \frac 1 m X   (a-y)^T 
\end{align}

$$

然后扩展到整个$W$，不难得出：

$$

\begin{align}
\frac {\partial J(W)} {\partial W^T}  &=  \frac 1 m X  (A-Y)^T \\
\frac {\partial J(W)} {\partial W}  &=  \frac 1 m (A-Y)  X^T
\end{align}

$$

上面推导主要用到了softmax函数的求导，详见[softmax函数导数](https://eipi10.cn/linear-algebra/2019/12/12/common_vector_derivative/#softmax函数)。

> 如果仔细观察，softmax的梯度其实和logistic regression的梯度其实也是结构完全相同，只是由于在softmax中$X,$和logistic regression中对应的$X$，刚好是进行了转置，所以梯度矩阵也进行了转置。而之所以要进行转置的原因之一，是因为softmax中是多个输出，在画图的时候，纵向排列的多个输出更加好画，易于表达。

## 历史

- 2020-10-18：初始创建。包含线性回归，逻辑回归，Softmax回归。

