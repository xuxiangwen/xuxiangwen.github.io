
#  Softmax回归 （Softmax Regression）

参考[Softmax回归](http://deeplearning.stanford.edu/wiki/index.php/Softmax%E5%9B%9E%E5%BD%92) 和 [Derivative of Softmax loss function](http://math.stackexchange.com/questions/945871/derivative-of-softmax-loss-function)。

$\begin{align}
h_\theta(x^{(i)}) =
\begin{bmatrix}
p(y^{(i)} = 1 | x^{(i)}; \theta) \\
p(y^{(i)} = 2 | x^{(i)}; \theta) \\
\vdots \\
p(y^{(i)} = k | x^{(i)}; \theta)
\end{bmatrix} =
\frac{1}{ \sum_{j=1}^{k}{e^{ \theta_j^T x^{(i)} }} }
\begin{bmatrix}
e^{ \theta_1^T x^{(i)} } \\
e^{ \theta_2^T x^{(i)} } \\
\vdots \\
e^{ \theta_k^T x^{(i)} } \\
\end{bmatrix}
\end{align} 
$ 

其中 $ \theta_1, \theta_2, \ldots, \theta_k \in R^{n+1} $ 是模型的参数。请注意
$\begin{align} 
\frac{1}{ \sum_{j=1}^{k}{e^{ \theta_j^T x^{(i)} }} } 
\end{align}$这一项对概率分布进行归一化，使得所有概率之和为 1 。

## 1. 方式一

$\begin{align}
J(\theta) = - \frac{1}{m} \left[ \sum_{i=1}^{m} \sum_{j=1}^{k}  1\left\{y^{(i)} = j\right\} \log \frac{e^{\theta_j^T x^{(i)}}}{\sum_{l=1}^k e^{ \theta_l^T x^{(i)} }}\right]
\end{align}  \\ 
p(y^{(i)} = j | x^{(i)} ; \theta) = \frac{e^{\theta_j^T x^{(i)}}}{\sum_{l=1}^k e^{ \theta_l^T x^{(i)}} }   
$

$
\begin{align}
J(\theta) = - \frac{1}{m} \left[ \sum_{i=1}^{m} \sum_{j=1}^{k} 1\left\{y^{(i)} = j\right\} \log \frac{e^{\theta_j^T x^{(i)}}}{\sum_{l=1}^k e^{ \theta_l^T x^{(i)} }}  \right] + \frac{\lambda}{2} \sum_{i=1}^k \sum_{j=0}^n \theta_{ij}^2
\end{align}
$

$
\begin{align}
\nabla_{\theta_j} J(\theta) = - \frac{1}{m} \sum_{i=1}^{m}{ \left[ x^{(i)} ( 1\{ y^{(i)} = j\}  - p(y^{(i)} = j | x^{(i)}; \theta) ) \right]  } + \lambda \theta_j
\end{align}
$

## 2. 方式二

### 2.1 基本设定
上面的方法看起来有些繁琐，下面方法更简洁。对于k分类问题，最后一层神经元的个数也为k。

设$Z \in  R^{k \times m}， \ \  A \in R^{k \times m},\ \  y \in R^{1 \times m} ,\ \  Z = W \cdot X$

### 2.2 转化y
y转换成Y，$Y \in R^{k \times m}， Y = \begin{bmatrix} y_1  , y_2  ,\ldots， y_i,\ldots  , y_m\ \     \end{bmatrix}$。

$b = 
\begin{bmatrix} 
1 \\ 1\\ 
\vdots\\
1
\end{bmatrix}, b \in R^{k \times 1}, \ 
kk = 
\begin{bmatrix} 
1 \\ 2\\ 
\vdots\\
k
\end{bmatrix}, kk \in R^{k \times 1}, \ 
c = 
\begin{bmatrix} 
1, 1, 1, \ldots, 1
\end{bmatrix}, c \in R^{1 \times m}  
$

$ Y = 
\begin{bmatrix} 
y=1 \\
y=2 \\
... \\
y=k 
\end{bmatrix} * 1  =  \left[ (b \cdot y) = (kk \cdot c) \right] * 1 $

举例来说。

如果$k =4， 
 y = \begin{bmatrix} 1, 1, 2, 2, 3, 3, 4, 4 \end{bmatrix} 
$ , 则$ Y = 
\begin{bmatrix} 
1, 1, 0, 0, 0, 0, 0, 0 \\
0, 0, 1, 1, 0, 0, 0, 0 \\
0, 0, 0, 0, 1, 1, 0, 0 \\
0, 0, 0, 0, 0, 0, 1, 1 
\end{bmatrix}   $  

### 2.3 Softmax函数

设$\ \begin{align}
d = 
\begin{bmatrix} 
1, 1, 1, \ldots, 1
\end{bmatrix}, d \in R^{1 \times k}  
\end{align}
$。

$
\begin{align}
A = h(Z) =   \frac {e^Z}  {d \cdot e^Z}
\end{align}
$ 这里的除法采用了matrix的broadcasting特性。

$
\begin{align}
J(W) = - \frac{1}{m}  \sum Y .* \log A = - \frac{1}{m}  \sum_{i=1}^m y_i^\mathrm{T} \cdot \log a_i 
\end{align}
$

成本函数采用交叉熵（cross entropy）

### 2.4 对$Z$的偏导数

设$
Z = \begin{bmatrix} z_1  , z_2  ,\ldots， z_i,\ldots   , z_m\ \   \end{bmatrix} , \ \  
A = \begin{bmatrix} a_1  , a_2  ,\ldots， a_i,\ldots   , a_m\ \   \end{bmatrix} , \ \  
X = \begin{bmatrix} x_1  , x_2  ,\ldots， x_i,\ldots   , x_m\ \   \end{bmatrix} , \ \ 
d^\mathrm{T} = \begin{bmatrix} 1, 1, ..., 1  \end{bmatrix}
$

每个$x_i, \ z_i, \ a_i$ 分别是第i个样本的输入向量，中间向量，输出向量。

先来观察单个样本
$
\begin{align}
a_i = h(z_i) =   \frac {e^{z_i}}  {\sum e^{z_i}}
\end{align}
$

$
\begin{align}
J_i = - y_i^\mathrm{T} \cdot \log a_i 
\end{align}
$

$
\begin{align}
\frac {\partial {J_i}} {\partial a_i} = -diag(\frac 1 {a_i}) \cdot y_i
\end{align}
$

$
\begin{align}
\frac {\partial {a_i}^\mathrm{T}} {\partial z_i} =  diag(a_i) - a_i \cdot {a_i}^\mathrm{T}
\end{align}
$

$
\begin{align}
\frac {\partial {J_i}} {\partial z_i} 
&= \frac {\partial {a_i}^\mathrm{T}} {\partial z_i}  \cdot \frac {\partial {J_i}} {\partial a_i} \\
&= (diag(a_i) - a_i \cdot {a_i}^\mathrm{T}) \cdot -diag(\frac 1 {a_i}) \cdot y_i \\
&=  a_i \cdot {a_i}^\mathrm{T} \cdot diag(\frac 1 {a_i}) \cdot y_i - y_i \\
&=  a_i \cdot d^\mathrm{T} \cdot y_i - y_i   
\end{align}
$

$由于  \sum y_i = 1， 故 d^\mathrm{T} \cdot y_i = 1  $

$\begin{align} \frac {\partial {J_i}} {\partial z_i} = a_i - y_i \end{align} $

对于所有样本，可以推出：

$
\begin{align}
\frac {\partial {J}} {\partial Z} 
&=  \frac 1 m (a - y)
\end{align}
$

这个结果非常好理解，预测误差越大，导数的（绝对值）越大；预测误差越小，导数越接近于0。 非常有意思的是，对于Linear Regression, Logistic Regression这两个回归，其梯度公式和这个完全一致。

###  2.5 对W的偏导数

再来观察单个神经元。

设$
A = \begin{bmatrix} a_1  \\ a_2  \\ \vdots \\  a_i \\ \vdots  \\ a_k\ \   \end{bmatrix} ,\ \
Y = \begin{bmatrix} y_1  \\ y_2  \\ \vdots \\  y_i \\ \vdots  \\ y_k\ \   \end{bmatrix} ,\ \
Z = \begin{bmatrix} z_1  \\ z_2  \\ \vdots \\  z_i \\ \vdots  \\ z_k\ \   \end{bmatrix} \ \ 
$, $z_j$是第j个神经元的中间向量，是一个行向量。
$W = \begin{bmatrix}
w_1 \\
w_2 \\
\vdots \\
w_k
\end{bmatrix} 
$， $w_j$是第j个神经元的参数，是一个行向量。

可以推出 $z_i = w_i \cdot X$

$
\begin{align}
\frac {\partial {J}} {\partial w_j} 
= \frac {\partial {J}} {\partial {z_i}} \cdot \frac {\partial {z_i}^\mathrm{T}} {\partial w_j} 
= \frac 1 m (a_i - y_i) \cdot X^\mathrm{T}
\end{align}
$

对于所有样本，可以推出：

$
\begin{align}
\frac {\partial {J}} {\partial W} 
&= \frac 1 m (A - Y) \cdot X^\mathrm{T}
\end{align}
$

仔细比较，其实发现和Logistric Regression完全相同。的确，Softmax Regression是Logistic Regression更加普遍的形式。

$\nabla{w} = \frac 1 m X^\mathrm{T} \cdot (h(Xw) - y) \ \ \ \ \ \ \ \  $   $\nabla{w}$是列向量， 这里的X和上面的X是转置关系。

$\textbf{神经网络中，为何经常采用softmax，而不是logistic regression作为最后的输出层呢？}$

目前的理解是，虽然它们偏导数公式完全相同，但由于softmax做了一个归一化处理，当计算$A−Y$时候，softmax的梯度调整会更加均衡。比方： 对于一个样本，两个神经元的输出分别是0.90, 0.45，对于Y是1, 0。当计算梯度时候，logistic得到结果是-0.1， 0.45，softmax得到结果是-0.333, 0.333。

logistic主要会调整第二个神经元的参数，第一个神经元几乎没有调整。而softmax会让两个神经元同时均匀的调整参数，这样似乎更好。

### 2.6 cross entropy 更加简洁的形式

下面是前面说的交叉熵求损失函数的，其实可以更加简单。

$
\begin{align}
J(W) = - \frac{1}{m}  \sum Y .* \log A = - \frac{1}{m}  \sum_{i=1}^m y_i^\mathrm{T} \cdot \log a_i 
\end{align}
$

 
$
\begin{align}
J(W) =  - \frac{1}{m} log \space {e^{a_{correct}} \over {\underset i \sum e^{a_i} } } 
\end{align}
$ 

$ 
\begin{align}
J(W) =  - a_{correct} + log {\underset i \sum e^{a_i} } 
\end{align}
$

It's called Log-softmax and it's better than naive log(softmax(a)) in all aspects:
* Better numerical stability
* Easier to get derivative right
* Marginally faster to compute

So why not just use log-softmax throughout our computation and never actually bother to estimate probabilities.

Here you are! We've defined the both loss functions for you so that you could focus on neural network part.

Since we want to predict probabilities, it would be logical for us to define softmax nonlinearity on top of our network and compute loss given predicted probabilities. However, there is a better way to do so.

If you write down the expression for crossentropy as a function of softmax logits (a), you'll see:

$$

 loss = - log \space {e^{a_{correct}} \over {\underset i \sum e^{a_i} } } 

$$

If you take a closer look, ya'll see that it can be rewritten as:

$$

 loss = - a_{correct} + log {\underset i \sum e^{a_i} } 

$$

It's called Log-softmax and it's better than naive log(softmax(a)) in all aspects:
* Better numerical stability
* Easier to get derivative right
* Marginally faster to compute

So why not just use log-softmax throughout our computation and never actually bother to estimate probabilities.

Here you are! We've defined the both loss functions for you so that you could focus on neural network part.

```python

```
