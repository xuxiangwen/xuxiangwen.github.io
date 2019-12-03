
# 反向传播（Back Propagation）

反向传播算法说起来，前前后后也成功推导过好些遍，但每次重新回忆起来，总是要花费不少时间。归根道底， 还是对矩阵之间求导的规则不是非常熟悉，目前而言，只是对向量之间求导比较熟练，对于矩阵求导，每次还需要分解到向量求导。不管如何，这次把基于向量求导的反向传播推导总结一下，以备以后回忆翻阅。

## 1. 网络基本情况

![network](http://d3kbpzbmcynnmx.cloudfront.net/wp-content/uploads/2015/09/nn-from-scratch-3-layer-network.png)

$n_l$是神经网络的总层数（包括一个输入层，若干个隐藏层和一个输出层，所以至少是两层）, $l$是指网络中的第$l$层，$S_l$是指第$l$层网络中神经元的个数。$ f(x) $是神经元的激活函数。

假设输入层$X \in  R^{n \times m}\ \ $(m个样本，每个样本是n维), $Y\in R^{S_{n_l} \times m} \ \ $ ($a^{(n_l)}$ 也是相同维度的矩阵)， 则

$ S_1 = n $ 

$ a^{(1)} \  $的维数是 $ {n\times m}$

$ z^{(l)} \  $的维数是 $ {S_{l} \times m}$

$ a^{(l)} \  $的维数是 $ {S_{l} \times m}$

$ W^{(l)} \  $的维数是 $ {S_{l+1} \times S_{l}}$

基本运算公式有：

$\frac {\mathrm{d} {f(x^\mathrm{T})}} {\mathrm{d}x} = diag(f'(x)), 其中
f'(x)=[\frac {\mathrm{d} f(x_1)} {\mathrm{d} x_1}, \frac {\mathrm{d} f(x_2)} {\mathrm{d} x_2}, \ldots, \frac {\mathrm{d} f(x_n)} {\mathrm{d} x_n} \  ] $    注：x是n维向量

$ a^1 = X $

$z^{(l+1)}=W^{(l+1)} \cdot  a^{(l)} + b^{(l+1)}
= W^{(l+1)} \cdot f(z^{(l)}) + b^{(l+1)}$ 

$a^{(l+1)} =f(z^{(l+1)}) $

$\begin{align} h_{W, b \ \  }(X) = a^{(n_l)} = f(z^{(n_l)}) \end{align}$

下面来看一下Cost函数：

$ J(W, b) = \frac {1} {2m}  \sum\limits_{i=1}^m (h_{W, b \ \ }(x_i)-y_i)^\mathrm{T}(h_{W, b \ \  }(x_i)-y_i)  $ 

正则化后公式为： 

$\begin{align}
J(W, b) = \frac 1 {2m} \sum\limits_{i=1}^m (h_{W, b \ \ }(x_i)-y_i)^\mathrm{T}(h_{W, b \ \  }(x_i)-y_i) +   \frac \lambda {2} \sum\limits_{l=1}^{n_l-1} 
\sum\limits_{i=1}^{S_{l+1}} 
\sum\limits_{j=1}^{S_{l}} 
{W_{ij}^{(l)}}^2  
\end{align}$

##  2. 算法推导

### 2.1 第一种方法

如果从每个神经元来看， 

设$Y = \begin{bmatrix} y_1  \\ y_2  \\ \ldots  \\ y_{s_{n_l}}  \end{bmatrix}, 
z^{(l)} = \begin{bmatrix} z_1^{(l)}  \\  z_2^{(l)}  \\ \ldots \\  z_{S_l}^{(l)}  \end{bmatrix},  
a^{(l)} = \begin{bmatrix} a_1^{(l)}  \\  a_2^{(l)}  \\ \ldots \\  a_{S_l}^{(l)}  \end{bmatrix},  
w^{(l)}=\begin{bmatrix} w_1^{(l)}  \\ w_2^{(l)}  \\ \ldots  \\ w_{S_{l+1}}^{(l)} \\ \end{bmatrix} 
$ ，
注：$ y_1,  z_1^{(l)}, a_1^{(l)}, w_1^{(l)}$ 都是行向量

$ J(W, b) = 
\frac 1 {2m} \sum\limits_{i=1}^{s_{n_l}} (a_i^{(n_l)}-y_i)^\mathrm{T}(a_i^{(n_l)}-y_i) = 
\frac 1 {2m} \sum\limits_{i=1}^{s_{n_l}} (f(z_i^{(n_l)})-y_i) ^\mathrm{T}(f(z_i^{(n_l)})-y_i)   $

具体的步骤参考$\href {http://ufldl.stanford.edu/wiki/index.php/%E5%8F%8D%E5%90%91%E4%BC%A0%E5%AF%BC%E7%AE%97%E6%B3%95}{UFLDL教程}$

### 2.2 第二种方法

采用第一种方法虽然能够正常推导，但里面有很多$\sum$，理解起来不那么直接。下面用另外一种方法进行推导。

设$
X = \begin{bmatrix} x_1  ， x_2  ，\ldots  ， x_m \ \  \end{bmatrix}, 
Y = \begin{bmatrix} y_1  ， y_2  ，\ldots  ， y_m \ \  \end{bmatrix} $

$
z^{(l)} = \begin{bmatrix} z_1^{(l)}  ，  z_2^{(l)}  ， \ldots ，  z_m^{(l)} \ \  \end{bmatrix}  ,  
a^{(l)} = \begin{bmatrix} a_1^{(l)}  ，  a_2^{(l)}  ， \ldots ，  a_m^{(l)}  \ \  \end{bmatrix} 
$ 

$ x_1, y_1,  z_1^{(l)}, a_1^{(l)}$ 都是列向量。先看单个样本的损失函数。

$ J_i(W, b) = \frac 1 {2m}  (h_{W, b \ }(x_i)-y_i)^\mathrm{T}(h_{W, b \ }(x_i)-y_i)  $ 

$\begin{align} \delta_i^{(n_l)} = \frac {\mathrm{d} J_i(W, b)} {\mathrm{d} z_i^{(n_l)}} 
=  \frac {\mathrm{d} {(a_i^{(n_l)})}^\mathrm{T}} {\mathrm{d} z_i^{(n_l)}} \cdot  \frac {\mathrm{d} J_i(W, b)} {\mathrm{d} a_i^{(n_l)}}  
=   \frac {\mathrm{d} {f(z_i^{(n_l)})}^\mathrm{T}} {\mathrm{d} z_i^{(n_l)}} \cdot \frac 1 {m} (a_i^{(n_l)}-y_i)   
\end{align}$

这里可以引用两个公式。

* 阿达马乘积
$
u^\mathrm{T} \cdot diag(v) = u^\mathrm{T} .* v^\mathrm{T} = v^\mathrm{T} .*  u^\mathrm{T}   \\
diag(v) \cdot u  =   v .* u = u .* v 
$

* 函数导数公式
$
\frac {\mathrm{d} {f(x^\mathrm{T})}} {\mathrm{d}x} = diag(f'(x)), 其中
f'(x)=[\frac {\mathrm{d} f(x_1)} {\mathrm{d} x_1}, \frac {\mathrm{d} f(x_2)} {\mathrm{d} x_2}, \ldots, \frac {\mathrm{d} f(x_n)} {\mathrm{d} x_n}  ] $    注：x是n维向量

这样可以推出： 

$
\delta_i^{(n_l)} 
=  \frac 1 {m}  {f'(z_i^{(n_l)})} .* (a_i^{(n_l)}-y_i) 
$

仔细观察上面公式，左右两个表达式的维度都是$S_{n_l} \times 1$, 这样很容易推广到m个样本的情况。这里的关键是理解阿达马乘积的特性。

$
\delta^{(n_l)} 
=  \frac 1 {m}  {f'(z^{(n_l)})} .* (a^{(n_l)}-Y) 
$

下面我们来看 $ \delta_i^{(l)} $, 因为$z_i^{(l)}$只用于计算对应的$z_i^{(l+1)}$，在求导的时候我们只需要把$z_i^{(l+1)}$作为中间变量即可。

$\begin{align} 
\delta_i^{(l)} &= \frac {\mathrm{d} J(W)} {\mathrm{d} z_i^{(l)}}  \\
&=  \frac {\mathrm{d} (z_i^{(l+1)}\ )^\mathrm{T}} {\mathrm{d} z_i^{(l)}} \cdot \frac {\mathrm{d} J_i(W, b)} {\mathrm{d} z_i^{(l+1)}}  \\
&=  \frac {\mathrm{d} {(W^{(l+1)} \cdot f(z_i^{(l)}\ ) + b^{(l+1)}\ )}^\mathrm{T}} {\mathrm{d} z_i^{(l)}} \cdot \delta_i^{(l+1)}  \\
&=  \frac {\mathrm{d} {f(z_i^{(l)})\ }^\mathrm{T}} {\mathrm{d} z_i^{(l)}}  
\cdot \frac {\mathrm{d} {(W^{(l+1)} \cdot f(z_i^{(l)}\ ) + b^{(l+1)}\ )}^\mathrm{T}} {\mathrm{d} f(z_i^{(l)})}
\cdot \delta_i^{(l+1)}  \\
&=  f'(z_i^{(l)}) .* \{(W^{(l+1)}\ )^\mathrm{T} \cdot \delta_i^{(l+1)} \  \} \\
&=  (W^{(l+1)} \ )^\mathrm{T} \cdot \delta_i^{(l+1)} \  .* f'(z_i^{(l)}) 
\end{align}$

再次仔细观察上面公式，左右两个表达式的维度都是$S_{l} \times 1$, 这样很容易推广到m个样本的情况。这里的关键也是理解阿达马乘积的特性。

$ \delta^{(l)} =  (W^{(l+1)} \ )^\mathrm{T} \cdot \delta^{(l+1)} \ .* f'(z^{(l)})   $

接下来看$w_i^{(l)}$的梯度。这一次$w_i^{(l)}$ 和 $z_i^{(l)}$ 是行向量。采用行向量的原因是，$w_i^{(l)}$是指一个神经元的参数，它只用于计算对应的$z_i^{(l+1)}$，在求导的时候我们只需要把$z_i^{(l+1)}$作为中间变量即可。

$ z^{(l)} = \begin{bmatrix} z_1^{(l)}  \\  z_2^{(l)}  \\ \ldots \\  z_{S_l}^{(l)}  \end{bmatrix},  
W^{(l)}=\begin{bmatrix} w_1^{(l)}  \\ w_2^{(l)}  \\ \ldots  \\ w_{S_{l+1}}^{(l)} \\ \end{bmatrix}  $

$ \frac {\mathrm{d} J(W)} {\mathrm{d} w_i^{(l)}} 
=  \frac {\mathrm{d} J(W)} {\mathrm{d} z_i^{(l)} } \cdot  \frac {\mathrm{d} {z_i^{(l)}\ }^\mathrm{\ \ T}} {\mathrm{d} w_i^{(l)}} 
=  \delta_i^{(l)} \cdot  (a^{(l-1)}\ )^\mathrm{T}   $   , 注：$z_i^{(l)}=w_i^{(l)} \cdot a^{(l-1)} + b_i^{(l)}$ 

$ \frac {\mathrm{d} J(W)} {\mathrm{d} b_i^{(l)}} 
=  \frac {\mathrm{d} J(W)} {\mathrm{d} z_i^{(l)}} \cdot  \frac {\mathrm{d} {z_i^{(l)}\ }^\mathrm{ \ \ T}} {\mathrm{d} b_i^{(l)}} 
=  \delta_i^{(l)} \cdot u  $  注：$ u = \begin{bmatrix} 1  \\  1  \\ \ldots \\ 1  \end{bmatrix}  $, u是$m$维向量

由上面的公式可以很容易扩展到矩阵的情况。

$ \frac {\mathrm{d} J(W)} {\mathrm{d} w^{(l)}} 
=  \delta^{(l)} \cdot  (a^{(l-1)}\ )^\mathrm{T}   $  

$ \frac {\mathrm{d} J(W)} {\mathrm{d} b^{(l)}} 
=  \delta^{(l)} \cdot u  $ 

这里设置两个新的矩阵:
$ \theta^{(l)} = \begin{bmatrix} b^{(l)}, w^{(l)} \end{bmatrix} $ , 
$ \  c^{(l-1)}= \begin{bmatrix} u^\mathrm{T}  \\  a^{(l-1)} \end{bmatrix}  $, 则上面的公式可以简化为： 

$ \frac {\mathrm{d} J(W)} {\mathrm{d} \theta^{(l)}} 
=  \delta^{(l)} \cdot  (c^{(l-1)}\ )^\mathrm{T}   $  

这样一来，一切都显得简单清晰。

## 3. 总结

总结起来，BP算法可以归纳为以下的内容（大部分和上面是重合的）。以后如果翻阅，直接从这里开始便可。

### 3.1 网络情况

$n_l$是神经网络的总层数（包括一个输入层，若干个隐藏层和一个输出层，所以至少是两层）, $l$是指网络中的第$l$层，$S_l$是指第$l$层网络中神经元的个数。$ f(x) $是神经元的激活函数。

假设输入层$X\in R^{n \times m}\ \ $(m个样本，每个样本是n维), $Y\in R^{S_{n_l} \times m} \ \  $($a^{(n_l)}也是相同维度的矩阵$)， 则

$ S_1 = n $ 

$ a^{(1)} \ $的维数是 $ {n\times m}$

$ z^{(l)} \ $的维数是 $ {S_{l} \times m}$

$ a^{(l)} \ $的维数是 $ {S_{l} \times m}$

$ W^{(l)} \ $的维数是 $ {S_{l+1} \times S_{l}}$

### 3.1 基本计算公式

$\frac {\mathrm{d} {f(x^\mathrm{T})}} {\mathrm{d}x} = diag(f'(x)), 其中
f'(x)=[\frac {\mathrm{d} f(x_1)} {\mathrm{d} x_1}, \frac {\mathrm{d} f(x_2)} {\mathrm{d} x_2}, \ldots, \frac {\mathrm{d} f(x_n)} {\mathrm{d} x_n}  ] $    注：x是n维向量

$ a^1 = X $

$z^{(l+1)}=W^{(l+1)} \cdot  a^{(l)} + b^{(l+1)}
= W^{(l)} \cdot f(z^{(l)}) + b^{(l)}$ 

$a^{(l+1)} =f(z^{(l+1)}) $

$ \theta^{(l)} = \begin{bmatrix} b^{(l)}, W^{(l)} \end{bmatrix} $

$ c^{(l)} = \begin{bmatrix} 1  \\  a^{(l)} \end{bmatrix} $

$ h_{W}(X) = a^{(n_l)} = f(z^{(n_l)})$

下面来看一下Cost函数：

$ J(W, b) = \frac 1 {2m} \sum\limits_{i=1}^m (h_{W, b\ }(x_i)-y_i)^\mathrm{T}(h_{W, b\ }(x_i)-y_i)  $ 

注：也可以采用交叉熵作为Cost函数，公式结构没有变化。

$L2$正则化后公式为： 

$\begin{align} 
J(W, b) = J(w, b) +   \frac \lambda {2} \sum\limits_{l=1}^{n_l-1} 
\sum\limits_{i=1}^{S_{l+1}} 
\sum\limits_{j=1}^{S_{l}} 
{W_{ij}^{(l)}}^2  
\end{align} 
$

### 3.2 核心计算公式

BP算法（加上正则项后）核心的三个公式是： 

$
\delta^{(n_l)} 
=  \frac 1 {m}  {f'(z^{(n_l)})} .* (a^{(n_l)}-Y) 
$

$ \delta^{(l)} = (W^{(l+1)}  \ )^\mathrm{T} \cdot \delta^{(l+1)}\ .* f'(z^{(l)})    $

$ \frac {\mathrm{d} J
(W, b)} {\mathrm{d} \theta^{(l)}} 
=  \delta^{(l)} \cdot  (c^{(l-1)} \ )^\mathrm{T} + \frac 1 {m} [0, W^{{l}}]  $  

初略查看了，感觉这两个实现都不是那么好。看来看去还是ufldl里的最好。

- $\href {https://github.com/mattm/simple-neural-network/blob/master/neural-network.py} {simple-neural-network\ python}$
- $\href {http://www.hankcs.com/ml/back-propagation-neural-network.html} {反向传播神经网络极简入门}$
- $\href {https://zhuanlan.zhihu.com/p/22473137} {神经网络反向传播的数学原理} $
- $\href {http://www.jianshu.com/p/9e217cfd8a49} {手写，纯享版反向传播算法公式推导}$
