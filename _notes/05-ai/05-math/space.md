---
title: 线性空间
categories: linear-algebra
date: 2020-06-28
---

本文将列举线性代数中所使用一些概念以及空间。每一个空间都有具体的数学含义，某种程度上，数学的发展就是建立在空间的不断扩展上的。

![image-20200813173938603](images/image-20200813173938603.png)

## 基本概念

### 共轭复数（Conjugate Complex ）

![img](images/220px-Complex_conjugate_picture.svg.png)

两个实部相等，虚部互为相反数的复数互为共轭复数。若$z=a+b\mathbf i (a，b \in \mathbb R)$，则它的共轭是 $\bar z = a -  b\mathbf i$。例如：
$$
\overline {3-2\mathbf i} = 3+2\mathbf i \\
\overline 7 = 7 \\
\overline i = i
$$
在复数的极坐标的下，复共轭写成
$$
\overline {re^{\mathbf i \theta}} = {re^{-\mathbf i \theta}}
$$
将复数理解为[复平面](https://zh.wikipedia.org/wiki/複平面)，则复共轭无非是对实轴的[反射](https://zh.wikipedia.org/wiki/反射_(数学))。

> 「共轭」是数学中一个比较有逼格的词。相信很多人和我一样第一次看到`共轭`一词，被吓坏了，根本不知道啥意思，因为这个词实际在中文中也用的很少。「轭」是牛拉车用的木头，同时拉一辆车的两头牛，就是「共轭」关系。
>
> ![img](images/v2-46d1570050f2e3f969587338dc746a0d_720w.jpg)
>
> 其实 Conjugate英文含义是结合，使成对。把这种关系引申到数学中，只要是成对的东西，又找不着一个更合适的叫法时，就常常称它们为「共轭」。具体到复数里，「共轭」就是「实部相同，虚部相反」的意思。

### 共轭转置（Conjugate Transpose）

方阵$A$的共轭转置$A^*$（又称埃尔米特共轭、埃尔米特转置），定义为
$$
A^*_{i, j} = \overline {A_{j, i}}
$$
也可以写成
$$
A^* = (\overline A)^T = \overline {A^T}
$$
很明显，当$A$时实数矩阵时，$A^* = A^T$。

下面是一个例子。
$$
A = \begin{bmatrix}  3+i & 5 \\ 2- 2i & i   \end{bmatrix}
$$
则
$$
A^*= \begin{bmatrix}  3-i & 2+2i  \\ 5 & -i   \end{bmatrix}
$$

### 埃尔米特矩阵（Hermitian Matrix）

又称厄米特矩阵，厄米矩阵，是[共轭](https://zh.wikipedia.org/wiki/共轭转置)[对称](https://zh.wikipedia.org/wiki/對稱矩陣)的[方阵](https://zh.wikipedia.org/wiki/方块矩阵)。埃尔米特矩阵中每一个第$i$行第*j*列的元素都与第$j$行第*i*列的元素的[复共轭](https://zh.wikipedia.org/wiki/共轭复数)。
$$
{A_{i, j}}= \overline {A_{j, i}}
$$
记为
$$
A^* = A
$$
例如：
$$
\begin{bmatrix} 
3 & 2+i \\
2-i & 1
\end{bmatrix}
$$
显然，**埃尔米特矩阵主对角线上的元素都是实数的，其特征值也是实数**。对于实数矩阵，对称矩阵是埃尔米特矩阵。

### 斜埃尔米特矩阵（Skew-Hermitian Matrix）

也称反埃尔米特矩阵。
$$
{A_{i, j}}= -\overline {A_{j, i}}
$$
记为
$$
A^* = -A
$$
例如：
$$
\begin{bmatrix} 
i & 2+i \\
-2+i & 3i
\end{bmatrix}
$$
**斜埃尔米特矩阵的特征值为零或虚数。**

### 酉矩阵（Unitary Matrix）

酉矩阵（又译作幺正矩阵）是一个 $n \times n$ [复数](https://zh.wikipedia.org/wiki/複數)[方块矩阵](https://zh.wikipedia.org/wiki/方块矩阵) $U$，其满足以下性质：
$$
U^*U = UU^* = I_n
$$
其中$ U^* $是 $U$ 的[共轭转置](https://zh.wikipedia.org/wiki/共轭转置)，$I_n$ 是 $n \times n$  单位矩阵。

换句话说，酉矩阵的[逆矩阵](https://zh.wikipedia.org/wiki/逆矩陣)，就是其共轭转置。酉矩阵是实数上的[正交矩阵](https://zh.wikipedia.org/wiki/正交矩阵)，在复数的推广。

以下是一个酉矩阵的例子：
$$
U = \begin{bmatrix} - \frac i {\sqrt 2}  & \frac 1 {\sqrt 2} \\ \frac i {\sqrt 2}  & \frac 1 {\sqrt 2}\end{bmatrix}
$$
验正如下：
$$
U^*U =\begin{bmatrix}  \frac i {\sqrt 2}  & \frac i {\sqrt 2}\\  \frac 1 {\sqrt 2}  & \frac 1 {\sqrt 2}\end{bmatrix}\begin{bmatrix} - \frac i {\sqrt 2}  & \frac 1 {\sqrt 2} \\ \frac i {\sqrt 2}  & \frac 1 {\sqrt 2}\end{bmatrix} =\begin{bmatrix} 1 & 0 \\ 0 & 1\end{bmatrix}  \\UU^* =\begin{bmatrix} - \frac i {\sqrt 2}  & \frac 1 {\sqrt 2} \\ \frac i {\sqrt 2}  & \frac 1 {\sqrt 2}\end{bmatrix}\begin{bmatrix}  \frac i {\sqrt 2}  & \frac i {\sqrt 2}\\  \frac 1 {\sqrt 2}  & \frac 1 {\sqrt 2}\end{bmatrix}=\begin{bmatrix} 1 & 0 \\ 0 & 1\end{bmatrix}
$$
总结起来：

- 在实数空间：A正交矩阵，B对称矩阵 

- 在复数空间：A酉矩阵 ，B共轭矩阵 

### 正规矩阵（Normal Matrix）

$A$是一个方阵，且$A$ 乘以自己的共轭转置 $ A^* $ 等于 $ A^* $ 乘以$A$。即
$$
A^∗A=AA^∗
$$

所有的[酉矩阵](https://zh.wikipedia.org/wiki/酉矩阵)、[埃尔米特矩阵](https://zh.wikipedia.org/wiki/埃尔米特矩阵)和[斜埃尔米特矩阵](https://zh.wikipedia.org/wiki/斜埃尔米特矩阵)都是正规的，但是正规矩阵并非只包括上述几类，比如下面的
$$
A^*  = 
\begin{bmatrix}  
1 & 1 & 0 \\  
0 & 1 & 1 \\  
1 & 0 & 1 
\end{bmatrix}
$$
是正规矩阵。
$$
AA^* = 
\begin{bmatrix}  2 & 1 & 1 \\  1 & 2 & 1 \\  1 & 1 & 2 \end{bmatrix}
= A^*A
$$

## 线性空间（Linear Space）

又称[向量空间](https://zh.wikipedia.org/wiki/%E5%90%91%E9%87%8F%E7%A9%BA%E9%97%B4)（Vector Space）。线性空间的一个直观模型是向量几何，几何上的向量及相关的运算即向量加法，标量乘法，以及对运算的一些限制如封闭性，结合律，已大致地描述了“向量空间”这个数学概念的直观形象。

在现代数学中，“向量”的概念不仅限于此，满足下列公理的任何数学对象都可被当作向量处理。譬如，实系数多项式的集合在定义适当的运算后构成向量空间，在代数上处理是方便的。单变元实函数的集合在定义适当的运算后，也构成向量空间，研究此类函数向量空间的数学分支称为[泛函分析](https://zh.wikipedia.org/wiki/泛函分析)。

线性空间必须满足以下性质。

|            公理            |                            说明                            |
| :------------------------: | :--------------------------------------------------------: |
|      向量加法的结合律      |               $u + (v + w) = (u + v) + w   $               |
|      向量加法的交换律      |                     $u + v = v + u  $                      |
|      向量加法的单位元      |             使得对任意$u ∈ V$都满足$u + 0 = u$             |
|      向量加法的逆元素      | 对任意$v \in V$都存在其逆元素$−v \in V$使得$v + (−v) = 0 $ |
| 标量乘法与标量的域乘法相容 |                      $a(bv) = (ab)v$                       |
|      标量乘法的单位元      |             域$F$存在乘法单位元$1$满足$1v = v$             |
| 标量乘法对向量加法的分配律 |                   $a(u + v) = au + av $                    |
|  标量乘法对域加法的分配律  |                   $ (a + b)v = av + bv $                   |

## 欧式空间（Euclidean Space）

设$V$是实数域$R$上的线性空间，在$V$上任意两向量$x$、$y$按某一确定法则对应于唯一确定的实数，称为内积，记为$（x，y）$，足以下性质：

- 对称性：$（x，y）=（y，x）$
- 可加性：$（x+y，z）=（x，z）+（y，z）$
- 齐次性：$（k x，y）=k（x，y）$，$k$为任意实数
- 非负性：$（x，x）≥ 0$，当且仅当$x=0$时为$0$

定义了内积的实线性空间$V$，叫实内积空间即欧式空间（有限维或无限维）。欧式空间的子空间仍是欧式空间。

## 酉空间（Unitary Space）

设$V$是复数域$C$上的线性空间，在$V$上任意两向量$x、y$按某一确定法则对应于唯一确定的复数，称为内积，记为$（x，y）$，满足以下性质：

- 对称性：$（x，y）=（y，x）$
- 可加性：$（x+y，z）=（x，z）+（y，z）$
- 齐次性：$（k x，y）=k（x，y）$，$k$为任意复数
- 非负性：$（x，x）≥ 0$，当且仅当$x=0$时为$0$

定义了内积的复线性空间$V$，叫复内积空间即酉空间（有限维或无限维）。

## 内积空间（Inner Product Space）

**内积空间**是数学中的线性代数里的基本概念，是增添了一个额外的结构的向量空间。这个额外的结构叫做**内积**或标量积。内积将一对向量与一个标量连接起来，允许我们严格地谈论向量的“夹角”和“长度”，并进一步谈论向量的正交性。内积空间由欧几里得空间抽象而来（内积是点积的抽象），这是[泛函分析](https://zh.wikipedia.org/wiki/泛函分析)讨论的课题。

酉空间和欧式空间统称为内积空间。

## 希尔伯特空间（Hilbert Space）

希尔伯特空间即完备的内积空间，也就是说一个带有内积的完备向量空间。希尔伯特空间就是由若干个函数作为独立坐标构成的抽象空间。

- 向量可以是有限维也可以是无限维，可以是实数，虚数，也可以是函数。

- 空间是完备的。所要描述的这类状态的所有可能值都被这个空间包含了。

   想象一下，我们愉快的生活在一张纸上的世界，以我们2维的视角，这个世界是完备的，所有东西的位置都是可描述的。某一天，一个不可描述的大能拿它沾了口水的手指在纸上戳了个洞。这个洞对我们而言就变成了未知。

## 赋范线性空间（Normed Linear Space）

赋范向量空间是具有"长度"概念的向量空间。$\mathbb{R}_n$中的长度被更抽象的范数替代。“长度”概念的特征是：

- 零向量的长度是零，并且任意向量的长度是非负实数。
- 一个向量 $v$ 乘以一个标量 $\alpha $时，长度应变为原向量 *v* 的 $\vert \alpha \vert$（ $\alpha $ 的绝对值）倍。
- 三角不等式成立。也就是说，对于两个向量 $v$ 和 $u $，它们的长度和（“三角形”的两边）大于 $v+u $（第三边）的长度。

## 巴拿赫空间（Banach Space）

在数学里，尤其是在泛函分析之中，巴拿赫空间是一个[完备](https://zh.wikipedia.org/wiki/完备空间)[赋范向量空间](https://zh.wikipedia.org/wiki/賦範向量空間)。更精确地说，巴拿赫空间是一个具有范数并对此范数完备的向量空间。其完备性体现在，空间内任意向量的[柯西序列](https://zh.wikipedia.org/wiki/柯西序列)总是收敛到一个良定义的位于空间内部的极限。

## 参考

- [如何直观地理解「共轭」这个概念？](https://www.zhihu.com/question/264249324)

- [欧式空间与酉空间——概念区分](https://blog.csdn.net/akadiao/article/details/74012240)

- [希尔伯特空间](https://zh.wikipedia.org/wiki/%E5%B8%8C%E5%B0%94%E4%BC%AF%E7%89%B9%E7%A9%BA%E9%97%B4)

- [通俗的解释希尔伯特空间](https://www.zhihu.com/question/27898379)

- [酉矩阵](https://zh.wikipedia.org/wiki/%E9%85%89%E7%9F%A9%E9%98%B5)

- [共轭复数](https://zh.wikipedia.org/wiki/%E5%85%B1%E8%BD%AD%E5%A4%8D%E6%95%B0)

  

