---
title: 迹
categories: linear-algebra
date: 2020-08-12
---

方阵的迹（trace）是方阵主对角线元素的总和。定义如下：

设方阵
$$
A = \begin{bmatrix} 
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n}  \\
\vdots & \vdots  & \ddots & \vdots \\
a_{n1} & a_{n2} & \cdots & a_{nn}  
\end{bmatrix}
$$
用$tr(A)$表示方阵$A$的迹，即：
$$
tr(A) = \sum_{i=1}^n\ a_{ii}  \tag 1
$$
迹等于方阵的特征值之和，设$\lambda_1, \lambda_2,  \cdots, \lambda_n$是方阵的特征值，迹还可以表示为：
$$
tr(A) =  \sum_{i=1}^n\ \lambda_i  \tag 2
$$
相关的证明，参见[特征值和特征向量](https://eipi10.cn/linear-algebra/2019/12/07/eigenvalue_and_eigenvector/)。

## 迹的性质

当$A，B$是$n\times n$矩阵，则
$$
tr(A) = tr(A^T)  \tag 3
$$

$$
tr(A + B) = tr(A) + tr(B) \tag 4
$$

$$
tr(r\cdot A) = r\cdot tr(A)  \tag 5
$$

当$A$是$m\times n$阶矩阵，而$B$是$n \times m$阶矩阵，则
$$
tr(AB) = tr(BA)  \tag 6
$$
其中$AB$是一个$m \times m$矩阵，而$BA$是一个$ n \times  n$矩阵。可以这样来理解。

设
$$
A = \begin{bmatrix} 
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n}  \\
\vdots & \vdots  & \ddots & \vdots \\
a_{m1} & a_{m2} & \cdots & a_{mn}  
\end{bmatrix} \\
 B^T = \begin{bmatrix} 
b_{11} & b_{12} & \cdots & b_{1n} \\
b_{21} & b_{22} & \cdots & b_{2n}  \\
\vdots & \vdots  & \ddots & \vdots \\
b_{m1} & b_{m2} & \cdots & b_{mn}  
\end{bmatrix} \\
 A \circ B^T = \begin{bmatrix} 
a_{11}b_{11} & a_{12}b_{12} & \cdots & a_{1n}b_{1n} \\
a_{21}b_{21} & a_{22}b_{22} & \cdots & a_{2n}b_{2n}  \\
\vdots & \vdots  & \ddots & \vdots \\
a_{m1}b_{m1} & a_{m2}a_{m2} & \cdots & a_{mn}b_{mn}  
\end{bmatrix}
$$
其中$\circ$表示[哈达玛积](https://baike.baidu.com/item/%E5%93%88%E8%BE%BE%E7%8E%9B%E7%A7%AF)，可以把trace的计算，看成是两个矩阵先进行哈达玛积，然后再进行累加，则：
$$
tr(AB)  = \sum A \circ B^T = \sum_{i=1}^m \sum_{j=1}^n a_{ij}b_{ij} =   tr(BA)
$$
由此，当$A，B，C$是$n\times n$矩阵，根据上式可得：
$$
tr(ABC) = tr(BCA) = tr(CAB) \tag 7
$$
当矩阵$A， B$是相似矩阵，即存在可逆矩阵$P$，使得$A = PBP^{-1}$，根据上式可得：
$$
tr(A) = tr(PBP^{-1}) = tr(P^{-1}PB) = tr(B)  \tag 8
$$
当$a，b$是向量，则：
$$
a^T b = tr(ab^T)  \tag 9
$$
向量的内积，可以看成迹。在矩阵计算中，往往大量采用内积的计算，内积变成迹，将极大的方便计算。

## 迹的导数

### Level 1

当$X$是$n\times n$矩阵，则：
$$
\frac {\partial tr(X)} {\partial X} = I_n \tag {10}
$$

$$
\frac {\partial tr(X^TX)} {\partial X} = 2X  \tag {11}
$$

$$
\begin{align}
\frac {\partial tr(X^2)} {\partial X} &= 2X^T  \tag {12}
\end{align}
$$

下面证明一下上面最后一个公式，设
$$
X = \begin{bmatrix} 
x_{11} & x_{12} & \cdots & x_{1n} \\
x_{21} & x_{22} & \cdots & x_{2n}  \\
\vdots & \vdots  & \ddots & \vdots \\
x_{n1} & x_{n2} & \cdots & x_{nn}  
\end{bmatrix}
$$
则
$$
\begin{align}
X\circ X^T &= \begin{bmatrix} 
x_{11}^2 & x_{12}x_{21} & \cdots & x_{1n}x_{n1} \\
x_{21}x_{12} & x_{22}^2 & \cdots & x_{2n}x_{n2}  \\
\vdots & \vdots  & \ddots & \vdots \\
x_{n1}x_{1n} & x_{n2} x_{2n} & \cdots & x_{nn}^2 
\end{bmatrix}
\end{align}
$$
不难发现，上面矩阵是对称矩阵，可以推得：
$$
\begin{align}
\sum X\circ X^T & = \sum_{i=1}^n x_{ii}^2 + 2\sum_{i=1}^n\sum_{j> i}^n x_{ij}x_{ji}
\end{align}
$$
再来计算导数，可得：
$$
\begin{align}
\frac {\partial tr(X^2)} {\partial X} &= \frac {\partial \sum (X\circ X^T)} {\partial X} \\ &= 2X^T
\end{align}
$$
当$X$是$m\times n$阶矩阵，而$A$是$n \times m$阶矩阵，则：
$$
\frac {\partial tr(XA)} {\partial X}  = A^T  \tag {13}
$$
当$A，B, X$是$n\times n$矩阵，则：
$$
\begin{align}
\frac {\partial tr(AXB)} {\partial X}  &= \frac {\partial tr(XBA)} {\partial X} 
\\ &= (BA)^T
\\ &= A^TB^T
\tag {14}
\end{align}
$$
同理可得：
$$
\begin{align}
\frac {\partial tr(AX^TB)} {\partial X}  &= BA
\tag {15}
\end{align}
$$

### Level 2

当$A，B, X$是$n\times n$矩阵，则：
$$
\begin{align}
\frac {\partial tr(X^2B)} {\partial X} &= (XB+BX)^T  \tag {16}
\end{align}
$$
下面证明一下上面最后一个公式，设
$$
B = \begin{bmatrix} 
b_{11} & b_{12} & \cdots & b_{1n} \\
b_{21} & b_{22} & \cdots & b_{2n}  \\
\vdots & \vdots  & \ddots & \vdots \\
b_{n1} & b_{n2} & \cdots & b_{nn}  
\end{bmatrix}
$$
可得：
$$
X^2 = \begin{bmatrix} 
\sum x_{1k} x_{k1} &   \sum x_{1k} x_{k2}  & \cdots & \sum x_{1k} x_{kj}  & \cdots & \sum x_{1k}x_{kn} \\
\sum x_{2k}x_{k1} & \sum x_{2k}x_{k2} & \cdots & \sum x_{2k} x_{kj} & \cdots  & \sum x_{2k}x_{kn}  \\
\vdots & \vdots  & \ddots & \vdots & \vdots & \vdots \\
\sum x_{ik}x_{k1} & \sum x_{ik}x_{k2} & \cdots& \sum x_{ik} x_{kj} & \cdots & \sum x_{ik}x_{kn}  \\
\vdots & \vdots & \vdots & \vdots& \ddots & \vdots \\
\sum x_{nk}x_{k1} & \sum x_{nk}x_{k2}  &  \cdots & \sum x_{nk} x_{kj} &  \cdots  & \sum x_{nk}x_{kn}  \\
\end{bmatrix}
$$

$$
X^2 \circ B^T  = \begin{bmatrix} 
b_{11}\sum x_{1k} x_{k1} &   b_{21}\sum x_{1k} x_{k2}  & \cdots & b_{j1}\sum x_{1k} x_{kj}  & \cdots & b_{n1}\sum x_{1k}x_{kn} \\
b_{12}\sum x_{2k}x_{k1} & b_{22}\sum x_{2k}x_{k2} & \cdots & b_{j2}\sum x_{2k} x_{kj} & \cdots  & b_{n2}\sum x_{2k}x_{kn}  \\
\vdots & \vdots  & \ddots & \vdots & \vdots & \vdots \\
b_{1i}\sum x_{ik}x_{k1} & b_{2i}\sum x_{ik}x_{k2} & \cdots& b_{ji}\sum x_{ik} x_{kj} & \cdots & b_{ni}\sum x_{ik}x_{kn}  \\
\vdots & \vdots & \vdots & \vdots& \ddots & \vdots \\
b_{1n}\sum x_{nk}x_{k1} & b_{2n}\sum x_{nk}x_{k2}  &  \cdots & b_{jn}\sum x_{nk} x_{kj} &  \cdots  & b_{nn}\sum x_{nk}x_{kn}  \\
\end{bmatrix}
$$

再来计算导数$\frac {\partial tr(X^2B)} {\partial x_{ij}}$，可以发现上面矩阵中仅第$i$行和第$j$列包含$x_{ij}$。

- 对于第$i$行，当$k=j$时包含$x_{ij}$，它们是：
  $$
  b_{1i}x_{ij} x_{j1} + b_{2i}x_{ij} x_{j2} + \cdots +  b_{ni}x_{ij}x_{jn}
  $$

- 对于第j行，当$k=i$时包含$x_{ij}$，它们是：
  $$
  b_{j1} x_{1i}x_{ij} + b_{j2} x_{2i}x_{ij} + \cdots +  b_{jn}x_{ni}x_{ij}
  $$

由上面两个公式可得：
$$
\begin{align}
\frac {\partial tr(X^2B)} {\partial x_{ij}}  = &\frac {\partial \sum (X^2 \circ B) } {\partial x_{ij} }
\\ = & b_{1i} x_{j1} + b_{2i} x_{j2} + \cdots +  b_{ni}x_{jn} + 
\\ &
b_{j1} x_{1i} + b_{j2} x_{2i} + \cdots +  b_{jn}x_{ni}
\end{align}
$$
其中最后两行分别代表：

- $ b_{1i} x_{j1} + b_{2i} x_{j2} + \cdots +  b_{ni}x_{jn}$代表矩阵$X$第$j$行和矩阵$B$第$i$列的内积。即
  $$
  b_{1i} x_{j1} + b_{2i} x_{j2} + \cdots +  b_{ni}x_{jn} =(B^T)_i \cdot (X^T)_j
  $$
  其中等式左边$i, j$分别代表相应矩阵的第$i$行和第$j$列。

- $b_{j1} x_{1i} + b_{j2} x_{2i} + \cdots +  b_{jn}x_{ni}$代表矩阵$B$第$j$行和矩阵$X$第$i$列的内积。即
  $$
  b_{j1} x_{1i} + b_{j2} x_{2i} + \cdots +  b_{jn}x_{ni} =(X^T)_i \cdot (B^T)_j
  $$
  其中等式左边$i, j$分别代表相应矩阵的第$i$行和第$j$列。

于是可以得到：
$$
\frac {\partial tr(X^2B)} {\partial x_{ij}}  =(B^T)_i \cdot (X^T)_j +(X^T)_i \cdot (B^T)_j
$$
最终我们可以推出：
$$
\begin{align}
\frac {\partial tr(X^2B)} {\partial X} &= B^TX^T+X^TB^T
\\ &= (XB+BX)^T 
\end{align}
$$
采用同样的推理方法，我们可以得到：
$$
\begin{align}
\frac {\partial tr(X^TBX)} {\partial X}  &= (B+B^T)X   \tag {17}
\end{align}
$$

$$
\begin{align}
\frac {\partial tr(XBX^T)} {\partial X}  &= X(B+B^T)   \tag {18}
\end{align}
$$

下面两个公式，实在有些复杂，目前只能背下了。
$$
\frac {\partial tr(AXBX)} {\partial X}  =  A^TX^TB^T + B^TX^TA^T \tag {19}
$$

$$
\frac {\partial tr(AX^TBX)} {\partial X}  =   BXA +B^TXA^T \tag {20}
$$

### Level 3

还有更加深入的一些公式。
$$
\frac {\partial tr(X^{-1})} {\partial X} =-(X^{-2})^T \tag {21}
$$

$$
\frac {\partial tr(AX^{-1}B)} {\partial X} =-(X^{-1}BAX^{-1})^T = -{(X^{-1})}^TA^TB^T{(X^{-1})}^T  \tag {22}
$$

## 参考

- [wiki: 迹](https://zh.wikipedia.org/wiki/%E8%B7%A1)
- [The Matrix Cookbook](https://www.math.uwaterloo.ca/~hwolkowi/matrixcookbook.pdf)
- [矩阵求导术（上）](https://zhuanlan.zhihu.com/p/24709748): 阐述了矩阵求导的原理。

