---
title: 特征值和特征向量
categories: linear-algebra
date: 2019-12-07
---

对于一个给定的$$n \times n $$方阵$$\mathbf A$$，对特征向量（eigenvector） $$\mathbf v$$进行线性变换之后，得到的新向量仍然与原来的$$\mathbf v$$保持在同一条直线上，但其长度或方向（即特征值eigenvalue）也许会改变。即 
$$
\underbrace{\mathbf{A}}_{n\times n}{\mathbf{v}} = \underbrace{\lambda}_{eigenvalue} \overbrace{\mathbf{v}}^{eigenvector}
$$
如果$$\mathbf A$$的列向量是线性无关的，则可以找到$$n$$个特征值，和对应的$$n$$个特征向量，这时公式变成：
$$
\mathbf{A} \mathbf{V} =  \mathbf{V} \mathbf {\Lambda}
$$
其中

- $$\mathbf V = \begin{bmatrix} \mathbf {v_1} & \mathbf {v_2} & \cdots & \mathbf {v_n} \end{bmatrix} $$，其中列向量分别代表$$n$$个特征向量，它们都是单位向量，$$\mathbf V $$称为特征向量矩阵。
- $$\mathbf {\Lambda} = diag(\mathbf {\lambda_1}, \mathbf {\lambda_2}, \cdots,  \mathbf {\lambda_n})$$，它是对角矩阵，对角线的值代表$$n$$个特征值。

光看上面的定义，不免觉得有些抽象。为了更好理解，首先来看相似矩阵。

## 相似矩阵

对于两个$$n\times n$$矩阵$$\mathbf A$$与$$\mathbf B$$，当且仅当存在一个$$n\times n$$的[可逆矩阵](https://zh.wikipedia.org/wiki/逆矩阵)$$\mathbf P$$，使得： 
$$
\mathbf {P^{-1}} \mathbf{A} \mathbf {P} = \mathbf{B}
$$
$$\mathbf P$$被称为矩阵$$\mathbf A$$和$$\mathbf B$$之间的**相似变换矩阵**，$$\mathbf A$$和$$\mathbf B$$之间互为**相似矩阵**。 可以这样来理解相似矩阵。

假设，在标准坐标系下，一个线性变换公式为$$\mathbf {\beta} = \mathbf A \mathbf \alpha $$，

而在坐标系$$\mathbf P $$下，同样这个线性变换的公式为$$\mathbf {\beta^{'}} = \mathbf B \mathbf {\alpha^{'}} $$，其中$$\mathbf {\beta^{'}}， \mathbf {\alpha^{'}} $$都是基于$$\mathbf  P$$坐标系上的坐标。

由于$$\mathbf {\beta^{'}}， \mathbf {\alpha^{'}} $$在标准坐标系中对应的坐标为$$\mathbf {\beta}， \mathbf {\alpha} $$，所以满足：
$$
\mathbf {\beta} =  \mathbf {P}  \mathbf {\beta^{'}}  \\
\mathbf {\alpha} =  \mathbf {P}  \mathbf {\alpha^{'}}
$$
然后可以进行如下推导。
$$
\begin{align}
\mathbf {P}  \mathbf {\beta^{'}} &= \mathbf A \mathbf \alpha  \\
\mathbf {P} (\mathbf B  \mathbf {\alpha^{'}}) &= \mathbf A (\mathbf P \mathbf {\alpha^{'}}) \\
\mathbf {P} \mathbf B &= \mathbf A \mathbf P \\
 \mathbf{B} &= \mathbf {P^{-1}} \mathbf{A} \mathbf {P}
 \end{align}
$$
所以**相似矩阵是同一个线性变换在不同坐标系（向量空间）下的表现形式**。存在这种情况，一个线性变换，在标准坐标系中，看起来非常复杂，而在某个坐标系（向量空间）中，却非常简单，而最简单的形式或许就是当$$\mathbf B$$是一个对角矩阵。

## 最简单的变换

接上文，当$$\mathbf B$$是对角矩阵， 记为$$\mathbf \Lambda$$。$$\mathbf {P} $$ 的各个列向量都是单位向量（模等于1的向量），记为$$\mathbf V$$。公式变为：
$$
\begin{align}
 \mathbf{\Lambda} &= \mathbf {V^{-1}} \mathbf{A} \mathbf {V} \\
\mathbf{A} \mathbf{V}  &=  \mathbf{V} \mathbf {\Lambda} 
 \end{align}
$$
刚好是特征向量和特征值的公式。也就是说，线性变换$$\mathbf A$$相当于向量空间$$\mathbf V$$中的一个缩放（对角矩阵$$\mathbf B$$），这样的变换最简单了。而且：
$$
\begin{align}
\mathbf {\beta} &= \mathbf A \mathbf \alpha \\
\mathbf {\beta} &= \mathbf {V} \mathbf{\Lambda} \mathbf { {V}^{-1} }\mathbf \alpha
\end{align}
$$
可以分为三步来解释：

- $$\mathbf { {V}^{-1}}\mathbf \alpha$$可以看成$$ \mathbf \alpha$$ 在坐标系$$\mathbf V$$中的坐标
- $$\mathbf{\Lambda} (\mathbf { {V}^{-1}}\mathbf \alpha)$$相当于对这个坐标进行了缩放
- $$\mathbf {V} (\mathbf{\Lambda} \mathbf { {V}^{-1}}\mathbf \alpha)$$相当于把缩放后的坐标，再映射回标准坐标系

这种空间变换的方式，不禁让人想起科幻小说[文明](https://book.douban.com/subject/25723455/ )里面提到的一种空战技术——`空闪`，大概意思是指战斗机在格斗的时候，跳跃到第四空间（超光速空间），然后再从第四空间跳跃回三维空间。在三维空间来看，这个战斗机瞬间消失了，然后瞬间出现在另外一个有利的攻击位置。

> 特征值，有可能是复数，对应的特征向量也是复数向量。

附[代码](https://nbviewer.jupyter.org/github/xuxiangwen/xuxiangwen.github.io/blob/master/_notes/05-ai/50-my-course/machine_learning/c0002.ipynb#特征值和特征向量)。

## 正交矩阵

当特征向量矩阵$$\mathbf V$$是正交矩阵，看看会发生什么。根据正交矩阵特性，$$\mathbf {V^{-1}} = \mathbf {V^T}$$，公式可以变为：
$$
\mathbf{A} =  \mathbf{V} \mathbf {\Lambda} \mathbf{V^T}
$$
而且，由于$$\mathbf V$$是正交矩阵，所以，$$\mathbf V$$和$$\mathbf {V^{T}}$$也可以理解为旋转，则

- $$\mathbf { {V}^{T}}\mathbf \alpha$$可以看成对$$ \mathbf \alpha$$进行旋转。
- $$\mathbf{\Lambda} (\mathbf { {V}^{T}}\mathbf \alpha) $$相当于对这个坐标进行了缩放
- $$\mathbf {V} (\mathbf{\Lambda} \mathbf { {V}^{T}}\mathbf \alpha) $$相当于把缩放后的坐标，再进行反向旋转

下面进一步看看$$\mathbf A$$有什么特性。
$$
\begin{align}
\mathbf{A} &=  \mathbf{V} \mathbf {\Lambda} \mathbf{V^T}  \\
\mathbf{A} &=  
\begin{bmatrix}
\lambda_1\mathbf {v_1} & \lambda_2 \mathbf {v_2} & \cdots & \lambda_n \mathbf {v_n} \\
\end{bmatrix} 
\begin{bmatrix}
\mathbf {v_1^T} \\ \mathbf {v_2^T} \\ \vdots \\ \mathbf {v_n^T} \\
\end{bmatrix} \\
\mathbf{A} &=  \lambda_1\mathbf {v_1} \mathbf {v_1^T} + \lambda_1\mathbf {v_2} \mathbf {v_2^T} + \cdots \lambda_n\mathbf {v_n} \mathbf {v_n^T}  \\ 
\mathbf{A} &=  \sum_{i}^n \lambda_i\mathbf {v_i} \mathbf {v_i^T}
\end{align}
$$
由于$${(\mathbf {v_i} \mathbf {v_i^T})}^T = \mathbf {v_i} \mathbf {v_i^T} $$，所以$$\lambda_i\mathbf {v_i} \mathbf {v_i^T}$$是对称矩阵，因此当$$\mathbf A$$必然也是对称矩阵。那么反过来是否成立呢，即对称矩阵的特征向量矩阵是正交矩阵吗？

假设$$\mathbf{v_i}, \mathbf{v_j}$$是两个特征向量，对应的特征值为$$\mathbf {\lambda_i} , \mathbf {\lambda_j} $$，则
$$
\mathbf{A} \mathbf{v_i} = \mathbf {\lambda_i}   \mathbf{v_i}
$$
两边乘以$$\mathbf {v_{j}^T} $$
$$
\mathbf {v_{j}^T} \mathbf{A} \mathbf{v_i} = \mathbf {v_{j}^T}  \mathbf {\lambda_i}   \mathbf{v_i}
$$
由于$$\mathbf A$$是对称矩阵, 即$$\mathbf {A^T} = \mathbf A$$，则
$$
\mathbf {v_{j}^T} \mathbf{A^T} \mathbf{v_i} = \mathbf {\lambda_i} \mathbf {v_{j}^T}    \mathbf{v_i}  \\
(\mathbf{A} \mathbf {v_{j}} )^{\mathbf T} \mathbf{v_i} = \mathbf {\lambda_i}  \mathbf {v_{j}^T}   \mathbf{v_i}
$$
由于$$\mathbf{A} \mathbf{v_j} = \mathbf {\lambda_j}   \mathbf{v_j}$$，则
$$
(\mathbf {\lambda_j}   \mathbf{v_j}  )^{\mathbf T} \mathbf{v_i} =  \mathbf {\lambda_i}  \mathbf {v_{j}^T}   \mathbf{v_i} \\
  \mathbf {\lambda_j}   \mathbf{v_j}^{\mathbf T} \mathbf{v_i} =  \mathbf {\lambda_i}  \mathbf {v_{j}^T}   \mathbf{v_i} \\
    (\mathbf {\lambda_i}-\mathbf {\lambda_j})  \mathbf{v_j}^{\mathbf T} \mathbf{v_i} =  0
$$
下面分两种情况：

- 当$$\mathbf {\lambda_i} \not = \mathbf {\lambda_j}$$，可以得出两个向量必定是正交的。

$$
\mathbf{v_j}^{\mathbf T} \mathbf{v_i} =  0
$$

- 当$$\mathbf {\lambda_i}  = \mathbf {\lambda_j}$$

  两边乘以一个不为0的实数

  $$
      \mathbf{A} \mathbf{v_i} = \mathbf {\lambda_i}   \mathbf{v_i} 
  $$

  $$
      \mathbf{A} p \mathbf{v_i} = \mathbf {\lambda_i}  p \mathbf{v_i} \tag{1}
  $$

  同理，可以得到

  $$
      \mathbf{A} \mathbf{v_j} = \mathbf {\lambda_i}   \mathbf{v_j}
  $$

  $$
      \mathbf{A} q \mathbf{v_j} = \mathbf {\lambda_i}  q \mathbf{v_j} \tag{2}
  $$

  公式$$(1)$$，$$(2)$$合并，可以得到

  $$
  \mathbf{A} (p \mathbf{v_i} + q \mathbf{v_j} )= \mathbf {\lambda_i}   (p \mathbf{v_i} + q \mathbf{v_j} )
  $$
  显见$$p \mathbf{v_i} + q \mathbf{v_j} $$也是特征向量，它是$$\mathbf {v_i}$$和$$\mathbf {v_j}$$线性组合而来，也就是说$$\mathbf {v_i}$$和$$\mathbf {v_j}$$所在平面的任何一个向量都是特征向量，这个平面上和其它（特征值不同）的特征向量垂直。取平面上任意两个垂直的单位向量，把它们加入特征向量矩阵，则这个矩阵就是正交矩阵。

总结以上两种情况，可以得到：**对称矩阵，总可以找到一个正交矩阵作为其特征向量矩阵。**

> 正交矩阵和对角矩阵非常简单，易于理解，计算起来尤其方便。对于对称矩阵，特征向量和特征值分别代表了正交化，对角化。

附[代码](https://nbviewer.jupyter.org/github/xuxiangwen/xuxiangwen.github.io/blob/master/_notes/05-ai/50-my-course/machine_learning/c0002.ipynb#对称矩阵的特征向量)。

## 方阵的迹和行列式

特征值有两个重要性质：

- 方阵的迹等于特征值的之和
- 方阵的行列式等于特征值之积

其中方阵的迹（trace），是它的主对角线元素的总和，也等于它的特征值的总和。这两个性质的数学表示如下。

设可逆方阵
$$
A = \begin{bmatrix} 
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n}  \\
\vdots & \vdots  & \ddots & \vdots \\
a_{n1} & a_{n2} & \cdots & a_{nn}  
\end{bmatrix}
$$
，且$\lambda=(\lambda_1, \lambda_2,  \cdots, \lambda_n)$是其对应的$n$个特征矩阵，则：
$$
\left\{  
\begin{array}{lll}  
 \sum_{i=1}^n\ \lambda_i = \sum_{i=1}^n\ a_{ii}=tr(A)    \\
\prod_{i=1}^{n} \lambda_i = |A|
\end{array}  
\right.
$$
其中$tr(A)$称为矩阵$A$的迹。

### 探究

下面我们来探究一下，上面的公式是怎么来的。根据特征值的定义可得：
$$
\begin{align}
A v &=\lambda v \\
( \lambda - A)v &= 0 \\
\begin{bmatrix} 
\lambda - a_{11} & -a_{12} & \cdots & -a_{1n} \\
-a_{21} & \lambda-a_{22} & \cdots & -a_{2n}  \\
\vdots & \vdots  & \ddots & \vdots \\
-a_{n1} & -a_{n2} & \cdots & \lambda - a_{nn}  
\end{bmatrix} v &= 0
\end{align}
$$
由于$v$不为0，要满足上面的公式，要求左边的方阵，其秩必须小于$n$，也就说必须满足：
$$
\left | 
\begin{array}{cccc}
\lambda - a_{11} & -a_{12} & \cdots & -a_{1n} \\
-a_{21} & \lambda-a_{22} & \cdots & -a_{2n}  \\
\vdots & \vdots  & \ddots & \vdots \\
-a_{n1} & -a_{n2} & \cdots & \lambda - a_{nn}  
\end{array} 
\right | = 0 \tag 1
$$

> 还可以这样来推理：秩小于$n$，意味着方阵中的$n$个向量必须线性相关，也就说其中任意一个向量，必然可以用剩下的$n-1$个向量来表达，也就说，这个向量存在于$n-1$个向量构成的线性空间中。而行列式可以看成是方阵的行或列向量构成的n维立方体的有向体积，当一个向量存在于$n-1$个向量构成的线性空间中，则它们（这$n$个向量）无法构成一个n维立方体了，体积当然为0。想象一下，在三维空间中，三个向量在一条直线上，它们的体积肯定是0。

很明显，对于方程$(1)$，特征值$\lambda_1, \lambda_2, \cdots , \lambda_n$是它的解，即满足：
$$
\begin{align}
\left | 
\begin{array}{cccc}
\lambda - a_{11} & -a_{12} & \cdots & -a_{1n} \\
-a_{21} & \lambda-a_{22} & \cdots & -a_{2n}  \\
\vdots & \vdots  & \ddots & \vdots \\
-a_{n1} & -a_{n2} & \cdots & \lambda - a_{nn}  
\end{array} 
\right | & =  (\lambda-\lambda_1)(\lambda-\lambda_2)\cdots(\lambda-\lambda_n)
\\ & = \lambda^n - (\lambda_1+\lambda_2+\cdots+\lambda_n)\lambda^{n-1} + \sum_{i=1}^{n-2}b_{n-i}\lambda^{n-i}  + (-1)^n  \lambda_1\lambda_2 \cdots\lambda_n 
\\ & = \lambda^n -  \sum_{i=1}^n\ \lambda_i \lambda^{n-1}  + \sum_{i=1}^{n-2}c_{i}\lambda^{i}  +  (-1)^n \prod_{i=1}^{n} \lambda_i   \tag 2
\end{align}
$$
上面公式中，$c_{n-i}$表示$\lambda$的幂次数是$1, 2, \cdots, n-2$时的系数。由此，我们的问题变成，在满足上面公式的情况下，证明：
$$
\left\{  
\begin{array}{lll}  
 \sum_{i=1}^n\ \lambda_i =tr(A)    \\
\prod_{i=1}^{n} \lambda_i = |A|
\end{array}  
\right.
$$

### 二阶方阵

为了能够形象的理解，首先看最简单的情况，当矩阵为$2$阶方阵：
$$
\begin{align}
\left | 
\begin{array}{cccc}
\lambda - a_{11} & -a_{12}  \\
-a_{21} & \lambda - a_{22} \\
\end{array} 
\right | & = \lambda^2-(\lambda_1 +\lambda_2)\lambda + \lambda_1 \lambda_2 \\
\lambda^2-(a_{11}+a_{22})\lambda + a_{11}a_{22} - a_{12}a_{21} &= \lambda^2-(\lambda_1 +\lambda_2)\lambda + \lambda_1 \lambda_2
\end{align}
$$
可以得到：
$$
\left\{  
\begin{array}{lll}  
 \lambda_1 + \lambda_2 = a_{11}+{a_22} = tr(A)    \\
 \lambda_1  \lambda_2 = a_{11}a_{22} - a_{12}a_{21}= |A|
\end{array}  
\right.
$$
由此，二阶方阵满足迹（主对角线元素的总和）等于它的特征值的总和，行列式等于它的特征值的积。

### n阶方阵

下面来看$n$阶方阵。设
$$
\begin{align}
|B|=  \left | 
\begin{array}{cccc}
\lambda - a_{11} & -a_{12} & \cdots & -a_{1n} \\
-a_{21} & \lambda-a_{22} & \cdots & -a_{2n}  \\
\vdots & \vdots  & \ddots & \vdots \\
-a_{n1} & -a_{n2} & \cdots & \lambda - a_{nn}  
\end{array} 
\right | =  \left | 
\begin{array}{cccc}
b_{11} & b_{12} & \cdots & b_{1n} \\
b_{21} & b_{22} & \cdots & b_{2n}  \\
\vdots & \vdots  & \ddots & \vdots \\
b_{n1} & b_{n2} & \cdots & b_{nn}  
\end{array} 
\right |
\end{align}
$$
根据[行列式计算的定义](http://cynhard.com/2018/10/15/LA-Determinants-Basic/#n-%E9%98%B6%E8%A1%8C%E5%88%97%E5%BC%8F)，每一行取一个数，每次取的列必须不同，我们可以得到：
$$
|B| =\sum\limits (-1)^{\tau} b_{1p_1}b_{2p_2}\cdots b_{np_n}
$$
其中$p_1, p_2, \cdots, p_n$为自然数$1$到$n$的排列组合之一，$\tau$为这个排列的[逆序数](https://baike.baidu.com/item/%E9%80%86%E5%BA%8F%E6%95%B0)，这样的排列共有$n!$。通过观察不难发现，要获得$\lambda$的$n-1$次幂，$b_{1p_1}, b_{2p_2}, \cdots,  b_{np_n}$当且仅当满足下面的公式才满足：
$$
b_{1p_1} = b_{11}=  \lambda - a_{11} \\
b_{1p_2} = b_{22}=  \lambda - a_{22} \\
\vdots \\
b_{1p_n} = b_{nn}=  \lambda - a_{nn} \\
$$
由于$p_1, p_2, \cdots, p_n$是顺序的，所以逆序数为0，可以得到
$$
\begin{align}
b_{11}b_{22}\cdots b_{nn} &= (\lambda-a_{11})(\lambda-a_{22})\cdots(\lambda-a_{nn}) \\
&= \lambda^n - (a_{11}+a_{22}+\cdots+a_{nn})\lambda^{n-1} ++ \sum_{i=0}^{n-2}c_{i}\lambda^{i}   \\
&= \lambda^n -   \sum_{i=1}^n a_{ii}\lambda^{n-1} + \sum_{i=0}^{n-2}c_{i}\lambda^{i} 
\end{align}
$$
其中$c_{n-i}$表示$\lambda$的幂次数是$0, 1, 2, \cdots, n-2$时的系数。

然后再结合公式$(2)$，可得：
$$
\begin{align}
 \sum_{i=1}^n\ \lambda_i \lambda^{n-1} &= \sum_{i=1}^n a_{ii}\lambda^{n-1} \\
 \sum_{i=1}^n\ \lambda_i &=\sum_{i=1}^n a_{ii}  \\
  \sum_{i=1}^n\ \lambda_i &=tr(A) 
 \end{align}
$$
由此得证，$n$阶方阵的迹等于特征值的之和。

下面再来看行列式，由公式$(2)$我们可以得到：
$$
\begin{align}
\left | 
\begin{array}{cccc}
\lambda - a_{11} & -a_{12} & \cdots & -a_{1n} \\
-a_{21} & \lambda-a_{22} & \cdots & -a_{2n}  \\
\vdots & \vdots  & \ddots & \vdots \\
-a_{n1} & -a_{n2} & \cdots & \lambda - a_{nn}  
\end{array} 
\right | & =  \lambda^n -  \sum_{i=1}^n\ \lambda_i \lambda^{n-1}  + \sum_{i=1}^{n-2}c_{i}\lambda^{i}  +  (-1)^n \prod_{i=1}^{n} \lambda_i   
\end{align}
$$
当$\lambda$等于0，可得：
$$
\begin{align}
\left | 
\begin{array}{cccc}
- a_{11} & -a_{12} & \cdots & -a_{1n} \\
-a_{21} & -a_{22} & \cdots & -a_{2n}  \\
\vdots & \vdots  & \ddots & \vdots \\
-a_{n1} & -a_{n2} & \cdots &  - a_{nn}  
\end{array} 
\right | & =  (-1)^n \prod_{i=1}^{n} \lambda_i   \\
(-1)^n\left | 
\begin{array}{cccc}
 a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n}  \\
\vdots & \vdots  & \ddots & \vdots \\
a_{n1} & a_{n2} & \cdots &   a_{nn}  
\end{array} 
\right | & =  (-1)^n \prod_{i=1}^{n} \lambda_i \\
\left | A \right |  = \prod_{i=1}^{n} \lambda_i 
\end{align}
$$
由此得证，$n$阶方阵的行列式等于特征值之积。

## 参考

- [《新理解矩阵4》：相似矩阵的那些事儿](https://spaces.ac.cn/archives/1777)

- [线性代数中，特征值与特征向量在代数和几何层面的实际意义是什么](https://www.zhihu.com/question/20507061)

- [wiki: 迹](https://zh.wikipedia.org/wiki/%E8%B7%A1)

- [wiki: 行列式](https://zh.wikipedia.org/wiki/%E8%A1%8C%E5%88%97%E5%BC%8F)

- [线性代数 - 行列式基础](http://cynhard.com/2018/10/15/LA-Determinants-Basic/)

  

