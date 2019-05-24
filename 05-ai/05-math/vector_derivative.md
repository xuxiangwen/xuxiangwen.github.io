
# 向量导数

向量导数非常重要，是机器学习中进行梯度下降计算的基本单位。

$\href {https://www.math.uwaterloo.ca/~hwolkowi/matrixcookbook.pdf} {The\ Matrix\  Cookbook} $, 这本书里更加深入丰富的公式

## 1. 基本运算 

向量导数有些抽象，很多人觉得有些难懂。但这就像小孩子学习乘法一样，开始也觉得难懂，可一旦小孩子背熟99乘法表后，便能快速掌握乘法。向量导数也是如此，只要能理解基本远算公式，并熟练推导它们，一定可以快速掌握向量导数，甚至矩阵导数。

设 $
I  =
\begin{bmatrix} 
1 & 0 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 & 0 \\
0 & 0 & ... & 0 & 0 \\
0 & 0 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 1
\end{bmatrix}
,\  
e = 
\begin{bmatrix} 
1 \\
1 \\
... \\
1 \\
1 
\end{bmatrix}
,\  
diag(u) =   
\begin{bmatrix} 
u_1 & 0 & 0 & 0 & 0 \\
0 & ... & 0 & 0 & 0 \\
0 & 0 & u_i & 0 & 0 \\
0 & 0 & 0 & ... & 0 \\
0 & 0 & 0 & 0 & u_d
\end{bmatrix}
,\  
X =   
\begin{bmatrix} 
x_1^\mathrm{T} \\ 
...  \\
x_i^\mathrm{T}  \\
...  \\
x_m^\mathrm{T}  \\
\end{bmatrix}
,\  
\lVert {w} \rVert _{2} = w^\mathrm{T}w
$

$\frac{\mathrm{d}u^\mathrm{T}}{\mathrm{d}u} = \mathrm{I}$

$\frac{\mathrm{d}u}{\mathrm{d}u^\mathrm{T}} = \mathrm{I}$

$
\frac{\mathrm{d}(\mathrm{A}u)^\mathrm{T}}{\mathrm{d}u} = 
\frac{\mathrm{d}u^\mathrm{T}\mathrm{A}^\mathrm{T}}{\mathrm{d}u} = 
\mathrm{A}^\mathrm{T} 
$    

$\frac{\mathrm{d}\mathrm{A}u}{\mathrm{d}u^\mathrm{T}} = \mathrm{A}  $ 

$
\frac{\mathrm{d}u^\mathrm{T}v}{\mathrm{d}x} = 
\frac{\mathrm{d}u^\mathrm{T}}{\mathrm{d}x} \cdot v + \frac{\mathrm{d}v^\mathrm{T}}{\mathrm{d}x} \cdot u
$

$
\frac{\mathrm{d}x^\mathrm{T}x}{\mathrm{d}x} = 2x
$

$
\frac{\mathrm{d}x^\mathrm{T}Ax}{\mathrm{d}x} = 
\frac{\mathrm{d}x^\mathrm{T}}{\mathrm{d}x} \cdot Ax + \frac{\mathrm{d}(Ax)^\mathrm{T}}{\mathrm{d}x} \cdot x =
(A + A^\mathrm{T})\cdot x
$

## 2.复合函数求导  

复合函数求导的基本公式： 

$ \frac{\mathrm{d}f(g(u^\mathrm{T}))}{\mathrm{d}u} = 
\frac{\mathrm{d}g(u^\mathrm{T})}{\mathrm{d}u} \cdot  \frac{\mathrm{d}f(g(u^\mathrm{T}))}{\mathrm{d}g(u)} $

$ \frac{\mathrm{d}f(g(u))}{\mathrm{d}u^\mathrm{T}} = 
 \frac{\mathrm{d}f(g(u))}{\mathrm{d}g(u^\mathrm{T})}  \cdot  \frac{\mathrm{d}g(u)}{\mathrm{d}u^\mathrm{T}} $
 
这里面的规律是：如果被导的是列向量，从右到左展开复合求导；如果被导的是列向量，从左到右展开复合求导。

设 
$
A =  
\begin{bmatrix} 
a_1^\mathrm{T}\\
...\\
a_i^\mathrm{T}\\
...\\
a_m^\mathrm{T}
\end{bmatrix}
, 
v = Au = 
\begin{bmatrix} 
a_1^\mathrm{T} \cdot u\\
...\\
a_i^\mathrm{T} \cdot u\\\
...\\
a_m^\mathrm{T} \cdot u
\end{bmatrix}
,
w = f(u) 
,
x = f(Au)= f(v) 
$

$
\frac {\mathrm{d}f(u^\mathrm{T})} {\mathrm{d}u} =
\begin{bmatrix} 
\frac {\partial f(u_1)} {\partial u_1} & 0 & 0 & 0 & 0 \\
0 & ... & 0 & 0 & 0 \\
0 & 0 & \frac {\partial f(u_i)} {\partial u_i} & 0 & 0 \\
0 & 0 & 0 & ... & 0 \\
0 & 0 & 0 & 0 & \frac {\partial f(u_d)} {\partial u_d}
\end{bmatrix} =
diag(\frac {\partial f(u_1)} {\partial u_1}_, ... \frac {\partial f(u_i)} {\partial u_i}_, ... \frac {\partial f(u_d)} {\partial u_d})
$

$
\frac{\mathrm{d}f((Au)^\mathrm{T})}{\mathrm{d}u} = 
\frac{\mathrm{d}(\mathrm{A}u)^\mathrm{T}}{\mathrm{d}u}  \cdot \frac{\mathrm{d}f((Au)^\mathrm{T})}{\mathrm{d}Au} = 
A^\mathrm{T} \cdot \frac{\mathrm{d}f((Au)^\mathrm{T})}{\mathrm{d}Au}=
A^\mathrm{T} \cdot diag(\frac {\partial f(v_1)} {\partial v_1}_, ... \frac {\partial f(v_i)} {\partial v_i}_, ... \frac {\partial f(v_m)} {\partial v_m})
$



$
\frac{\mathrm{d}g(f(u^\mathrm{T}))}{\mathrm{d}u} = 
\frac{\mathrm{d}f(u^\mathrm{T})}{\mathrm{d}u}  \cdot \frac{\mathrm{d}g(f(u^\mathrm{T}))}{\mathrm{d}f(u)} = 
diag(\frac {\partial f(u_1)} {\partial u_1}_, ... \frac {\partial f(u_i)} {\partial u_i}_, ... \frac {\partial f(u_d)} {\partial u_d}) \cdot
diag(\frac {\partial g(w_1)} {\partial w_1}_, ... \frac {\partial g(w_i)} {\partial w_i}_, ... \frac {\partial g(w_d)} {\partial w_d})
$


$
\frac{\mathrm{d}g(f((Au)^\mathrm{T}))}{\mathrm{d}u} = 
\frac{\mathrm{d}f((Au)^\mathrm{T})}{\mathrm{d}u}  \cdot \frac{\mathrm{d}g(f((Au)^\mathrm{T}))}{\mathrm{d}f(Au)} = 
A^\mathrm{T} \cdot diag(\frac {\partial f(v_1)} {\partial v_1}_, ... \frac {\partial f(v_i)} {\partial v_i}_, ... \frac {\partial f(v_m)} {\partial v_m}) \cdot diag(\frac {\partial g(x_1)} {\partial x_1}_, ... \frac {\partial g(x_i)} {\partial x_i}_, ... \frac {\partial g(x_m)} {\partial x_m})
$



阿达马乘积, 它具有对称性。

$
u^\mathrm{T} \cdot diag(v) = u^\mathrm{T} .* v^\mathrm{T} = v^\mathrm{T} .*  u^\mathrm{T}   \\
diag(v) \cdot u  =   v .* u = u .* v
$

### 实际例子

$\frac{\mathrm{d}\log(u^\mathrm{T})}{\mathrm{d}u} = 
\begin{bmatrix} 
1/u_1 & 0 & 0 & 0 & 0 \\  
0 & ... & 0 & 0 & 0 \\
0 & 0 & 1/u_i & 0 & 0 \\
0 & 0 & 0 & ... & 0 \\
0 & 0 & 0 & 0 & 1/u_d
\end{bmatrix} 
= diag(1/u)
$

$\frac{\mathrm{d}\log((Au)^\mathrm{T})}{\mathrm{d}u} = 
\frac{\mathrm{d}(Au)^\mathrm{T}}{\mathrm{d}u} \cdot \frac {\mathrm{d}\log((Au)^\mathrm{T})} {\mathrm{d}Au} = 
A^\mathrm{T} \cdot diag(1/Au) 
$


## 3. 矩阵导数

比起向量导数，矩阵的导数更加难以表达，很多时候是一个超矩阵。超矩阵是指矩阵里面的每个元素本身也是矩阵。它也有一些基本的运算公式。目前很多公式也是推断，还需要找更多相关书来阅读一下。



设 $ A \in R^{m \times n} $

$ \mathrm{II} = \mathrm{II}_{n^2 \times m^2} = \mathrm{II}_{m^2 \times n^2} $

$\frac{\mathrm{d}A^\mathrm{T}}{\mathrm{d}A} = \mathrm{II}$

$\frac{\mathrm{d}A}{\mathrm{d}A^\mathrm{T}} = \mathrm{II} $

$
\frac{\mathrm{d}(\mathrm{A}u)^\mathrm{T}}{\mathrm{d}A} = 
\frac{\mathrm{d}u^\mathrm{T}\mathrm{A}^\mathrm{T}}{\mathrm{d}A} = 
\mathrm{u}^\mathrm{T} 
$    

$\frac{\mathrm{d}\mathrm{A}u}{\mathrm{d}A^\mathrm{T}} = \mathrm{u} $ 

$
\frac{\mathrm{d}u^\mathrm{T}v}{\mathrm{d}A} = 
\frac{\mathrm{d}u^\mathrm{T}}{\mathrm{d}A} \cdot v + \frac{\mathrm{d}v^\mathrm{T}}{\mathrm{d}A} \cdot u
$

$
\frac{\mathrm{d}A^\mathrm{T}A}{\mathrm{d}A} = 2A  ？
$



上面的$\mathrm{II}$是一个超矩阵，它的绝对维度是$ (m \times n) \times (m \times n) $。 感觉它是一个变形金刚，它可以变成任意的形式，可以把它看成是一个$ m \times m $的矩阵，则每个元素是$ n \times n $，也可以把它看成是一个$ n \times n $的矩阵，则每个元素是$ m \times m $。它能和维度为m的向量相乘，也能和维度为n的向量相乘。而这些相乘都不会改变结果。 

$
\mathrm{II}  =
\begin{bmatrix} 
\mathrm{I} & 0 & 0 & 0 & 0 \\
0 & \mathrm{I} & 0 & 0 & 0 \\
0 & 0 & ... & 0 & 0 \\
0 & 0 & 0 & \mathrm{I} & 0 \\
0 & 0 & 0 & 0 & \mathrm{I}
\end{bmatrix}
$ 


看一个具体的例子，下面第一个公式非常容易已知的向量导数推出，但下面的第二个公式就没有这么容易了，因为X是一个矩阵。

$\frac{\mathrm{d}(Xw)^\mathrm{T}Xw}{\mathrm{d}w} =  \frac{\mathrm{d}w^\mathrm{T}X^\mathrm{T}Xw}{\mathrm{d}w} = 2X^\mathrm{T}Xw $

$\frac{\mathrm{d}(Xw)^\mathrm{T}Xw}{\mathrm{d}X} =  \frac{\mathrm{d}w^\mathrm{T}X^\mathrm{T}Xw}{\mathrm{d}X} = 2Xww^\mathrm{T}$

上面的公式有三个非常好理解的推导方法。

设$J=(Xw)^\mathrm{T}Xw $

另外一种想法，关于矩阵和矩阵之间导数，可以转化成向量之间的导数。即把矩阵先变成向量，然后求两个向量的导数，然后再根据需要把向量变成相关矩阵。


### 方法一
这个方法的来源于李飞腾的https://zhuanlan.zhihu.com/p/22473137 。他提出一个维数相容原则。

维数相容原则：通过前后换序、转置 使求导结果满足矩阵乘法且结果维数满足下式：

如果$x\in R^{m\times n}，  f(x)\in R^1，$ 那么 $\frac{\partial f(x)}{\partial x} \in R^{m\times n}$。

利用维数相容原则解上例：

step1：把所有参数当做实数来求导. ，$J=(Xw)^2$，

$\frac{\mathrm{d} J}{\mathrm{d} X}=2Xw^2$

step2：根据step1的求导结果，依据维数相容原则做调整：前后换序、转置

依据维数相容原则$\frac{\mathrm{d} J}{\mathrm{d} X} \in R^{m \times n}$，但$\frac{\mathrm{d} J}{\mathrm{d} X} \in R^{m \times n} = 2Xw^2$中$(Xw-y)\in R^{m \times 1}, w \in R^{n \times 1}$，自然得调整为$\frac{\mathrm{d} J}{\mathrm{d} X}=2Xww^T$；

### 方法二

方法一看起来有些主观猜测，可以让这个过程更加严谨一些。

设 $X = \begin{bmatrix} x_1, x_2, ..., x_n \end{bmatrix}  $

$\frac{\mathrm{d} J}{\mathrm{d} X}= \begin{bmatrix} \frac {\mathrm{d} J} {\mathrm{d} x_1}, \frac {\mathrm{d} J} {\mathrm{d} x_2}, ..., \frac {\mathrm{d} J} {\mathrm{d} x_n} \end{bmatrix}$

$ \frac {\mathrm{d} J} {\mathrm{d} x_i} =  \frac {\mathrm{d} (Xw)^\mathrm{T}} {\mathrm{d} x_i} \cdot  \frac {\mathrm{d} J} {\mathrm{d} Xw} = 
  \frac {\mathrm{d} (x_1w_1 + x_2w_2 + ... + x_iw_i + ... + x_nw_n)^\mathrm{T}} {\mathrm{d} x_i} \cdot 2Xw = 2w_iXw$
  
根据上面两个公式可以推出
$\frac{\mathrm{d} J}{\mathrm{d} X}= 2Xww^T $

### 方法三

可以让这个过程更加简单一些。根据复合函数求导公式，如果把X看成行向量（因为w是列向量，所以X看成行向量比较合适），则

$\frac {\mathrm{d}J} {\mathrm{d}X} = 
\frac {\mathrm{d}J} {\mathrm{d}Xw}  \cdot \frac {\mathrm{d}(Xw)^\mathrm{T}} {\mathrm{d}X} =
2Xw \cdot  \frac {\mathrm{d}(Xw)^\mathrm{T}} {\mathrm{d}X} =  2Xww^\mathrm{T} $

## 4. 梯度下降（Gradient Descent） 

### 4.1 线性回归 （Linear Regression）

$L(w) = \frac 1 {2m} (Xw - y)^\mathrm{T}(Xw - y) $

$\nabla{w} = \frac 1 m X^\mathrm{T}(Xw - y)  $ 

$ w|_{\nabla{w} = 0}  = (X^\mathrm{T}X )^{-1}X^\mathrm{T}y$

### 4.2 岭回归 （Ridge Regression）

$L(w) = \frac 1 {2m} (Xw - y)^\mathrm{T}(Xw - y) + \frac \lambda {2m}\lVert {w} \rVert _{2}$

$\nabla{w} = \frac 1 m X^\mathrm{T}(Xw - y) + \frac \lambda m w$ 

$ w|_{\nabla{w} = 0}  = (X^\mathrm{T}X + \lambda)^{-1}X^\mathrm{T}y$

### 4.3 Lasso回归

$L(w) = \frac 1 {2m} (Xw - y)^\mathrm{T}(Xw - y) + \frac \lambda {m}\lVert {w} \rVert _{1}$

$\nabla{w} = \frac 1 m X^\mathrm{T}(Xw - y) + \frac \lambda m ?$ 

$ w|_{\nabla{w} = 0}  = (X^\mathrm{T}X + ?)^{-1}X^\mathrm{T}y$

### 4.4 感知机（Perceptron）

设 $ y \in \{-1， 1\}$

$L(w) = -{(Xw)^\mathrm{T} \cdot y}|_{sign(Xw)<>y} = -{(Xw)^\mathrm{T} \cdot y}|_{y^\mathrm{T}Xw<=0}  = - \sum_i^m \min(0, y_ix_i^\mathrm{T}w)$

$\nabla{w} =  -{X^\mathrm{T} y}|_{sign(Xw)<>y} =  -{X^\mathrm{T} y}|_{y^\mathrm{T}Xw<=0} $ 

###  4.7 基于内容的推荐 （Content-based Recommendation）

# 参考

1.  $\href {http://blog.csdn.net/u010976453/article/details/54381248}{机器学习中的线性代数之矩阵求导}$ 



```python

```
