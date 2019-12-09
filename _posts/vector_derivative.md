---
title: 向量导数
categories: linear-algebra
date: 2019-12-09
---

向量导数非常重要，是机器学习中进行梯度下降计算的基本方式。

### 基本运算

向量导数有些抽象，很多人觉得有些难懂。但这就像小孩子学习乘法一样，开始也觉得难懂，可一旦小孩子背熟99乘法表后，便能快速掌握乘法。向量导数也是如此，只要能理解基本远算公式，并熟练推导它们，一定可以快速掌握向量导数，甚至矩阵导数。

设
$$
\mathbf u = \begin{bmatrix} u_1 \\ u_2 \\ \vdots \\ u_n \end{bmatrix},\ 
\mathbf v = \begin{bmatrix} u_1 \\ u_2 \\ \vdots \\ u_n \end{bmatrix},\ 
\mathbf w = \begin{bmatrix} w_1 \\ w_2 \\ \vdots \\ w_n \end{bmatrix}
$$
则，行向量对于列向量得导数定义如下：
$$
\frac{\partial \mathbf {u}^\mathbf{T} }{\partial \mathbf {w} } = 
\begin{bmatrix}
\frac{\partial  {u_1} }{\partial {w_1} } & 
\frac{\partial {u_2} }{\partial {w_1} } &
\cdots & 
\frac{\partial {u_n} }{\partial {w_1} } \\
\frac{\partial  {u_1} }{\partial {w_2} } & 
\frac{\partial {u_2} }{\partial {w_2} } &
\cdots & 
\frac{\partial {u_n} }{\partial {w_2} } \\
\vdots & \vdots & \ddots & \vdots \\
\frac{\partial  {u_1} }{\partial {w_n} } & 
\frac{\partial {u_2} }{\partial {w_n} } &
\cdots & 
\frac{\partial {u_n} }{\partial {w_n} } 
\end{bmatrix}
$$
上面公式中，行向量$$\mathbf {u}^\mathbf{T}$$的每一个成员和列向量$$\mathbf {w}$$的每一个成员分别进行求导，这样其结果刚好是一个矩阵。进一步推导，可以得到下面的公式：

$$\frac{\partial \mathbf {u}^\mathbf{T} }{\partial \mathbf {u} } = \frac{\partial \mathbf {v}^\mathbf{T} }{\partial \mathbf {v} } = \frac{\partial \mathbf {w}^\mathbf{T} }{\partial \mathbf {w} } = \mathbf{I_n} $$

$$\frac{\partial \mathbf {u}^\mathbf{T}\mathbf {v} }{\partial \mathbf {w} } = 
\frac{\partial \mathbf {u}^\mathbf{T} }{\partial \mathbf {w} } \cdot \mathbf {v} + \frac{\partial \mathbf {v}^\mathbf{T} }{\partial \mathbf {w} } \cdot \mathbf {u} $$

$$\frac{\partial \mathbf {w}^\mathbf{T}\mathbf {w} }{\partial \mathbf {w} } = 2\mathbf {w}$$

再设，$$\mathbf A$$是$$m \times n$$阶矩阵，$$\mathbf B$$是$$n \times n $$阶方阵，而且它们的每个元素不包含对于$$\mathbf w $$的表达式，可以推得：

$$\frac{\partial (\mathbf{A}\mathbf {w})^\mathbf{T} }{\partial \mathbf {w} } = 
\frac{\partial \mathbf {w}^\mathbf{T}\mathbf{A}^\mathbf{T} }{\partial \mathbf {w} } = 
\mathbf{A}^\mathbf{T}  $$

$$\frac{\partial \mathbf{A}\mathbf {w} }{\partial \mathbf {w}^\mathbf{T} } = \mathbf{A}  $$

$$\frac{\partial \mathbf {w}^\mathbf{T} \mathbf{B} \mathbf {w} } {\partial \mathbf {w} } = 
\frac {\partial \mathbf {w}^\mathbf{T} } {\partial \mathbf {w} } \cdot \mathbf{B} \mathbf {w} +
\frac {\partial (\mathbf{B} \mathbf {w})^\mathbf{T} } {\partial \mathbf {w} } \cdot \mathbf {w}=
(\mathbf{B} + \mathbf{B}^\mathbf{T})\cdot \mathbf {w}$$

###  复合函数

首先定义一下列向量对于列向量的导数：
$$
\frac{\partial \mathbf {u} }{\partial \mathbf {w} } = 
\begin{bmatrix}
\frac{\partial  {u_1} }{\partial {w_1} } \\
\frac{\partial  {u_2} }{\partial {w_2} } \\
\vdots \\
\frac{\partial  {u_n} }{\partial {w_n} }
\end{bmatrix}
$$
上面公式中，向量$$\mathbf {u}$$的每一个成员和向量$$\mathbf {w}$$的每一个成员一一进行求导，其结果是一个同阶的向量。下面来看函数。A

设$$f, g$$是函数，其输入是向量或矩阵，输出也是同阶的向量或矩阵（比如：$$\mathbf A$$是$$m \times n$$阶矩阵， 则$$f(\mathbf {A})$$也是$$m \times n$$阶矩阵）。

则

- 被导的是列向量，从右到左展开复合求导

$$
  \frac{\partial f(g(\mathbf {w}^\mathbf{T}))}{\partial \mathbf {w} } = 
  \frac{\partial g(\mathbf {w}^\mathbf{T})}{\partial \mathbf {w} } \cdot  \frac{\partial f(g(\mathbf {w}^\mathbf{T}))}{\partial g(\mathbf {w})}  
$$

- 被导的是行向量，从左到右展开复合求导

$$
\frac{\partial f(g(\mathbf {w}))}{\partial \mathbf {w}^\mathbf{T} } = 
   \frac{\partial f(g(\mathbf {w}))}{\partial g(\mathbf {w}^\mathbf{T})}  \cdot  \frac{\partial g(\mathbf {w})}{\partial \mathbf {w}^\mathbf{T} }
$$

可以推得：

$$
\begin{align}
\frac {\partial f(\mathbf {u}^{\mathbf {T} })} {\partial \mathbf {u} } &=
\begin{bmatrix} 
\frac {\partial f(\mathbf {u}_1)} {\partial \mathbf {u}_1} & 0 & \cdots & 0  \\
0 &  \frac {\partial f(\mathbf {u}_2)} {\partial \mathbf {u}_2} & \cdots & 0 \\
\vdots & \vdots  & \ddots & \vdots    \\
0 & 0 & 0 & \frac {\partial f(\mathbf {u}_n)} {\partial \mathbf {u}_n}
\end{bmatrix}  \\
\frac {\partial f(\mathbf {u}^{\mathbf {T} })} {\partial \mathbf {u} } &= 
diag(
\frac {\partial f(\mathbf {u}_1)} {\partial \mathbf {u}_1},  \frac {\partial f(\mathbf {u} _2)} {\partial \mathbf {u}_2}, \cdots, \frac {\partial f(\mathbf {u}_n)} {\partial \mathbf {u}_n}) \\
\frac {\partial f(\mathbf {u}^{\mathbf {T} })} {\partial \mathbf {u} } &= diag(\frac {\partial f(\mathbf {u})} {\partial \mathbf {u} })
\end{align}
$$

然后可以推得：

$
\frac{\partial f((\mathbf {Au})^\mathbf{T})}{\partial {\mathbf {u}}} = 
\frac{\partial (\mathbf{A}u)^\mathbf{T}}{\partial {\mathbf {u}}}  \cdot \frac{\partial f((\mathbf {Au})^\mathbf{T})}{\partial \mathbf {Au}} = 
\mathbf A^\mathbf{T} \cdot \frac{\partial f((\mathbf {Au})^\mathbf{T})}{\partial \mathbf {Au}}=
\mathbf A^\mathbf{T} \cdot diag(\frac{\partial f(\mathbf {Au})}{\partial \mathbf {Au}})       
$

$
\frac{\partial g(f(\mathbf {u}^\mathbf{T}))}{\partial {\mathbf {\mathbf {u}}}} = 
\frac{\partial f(\mathbf {u}^\mathbf{T})}{\partial {\mathbf {\mathbf {u}}}}  \cdot \frac{\partial g(f(\mathbf {u}^\mathbf{T}))}{\partial f(\mathbf {u})} = 
diag(\frac{\partial f(\mathbf {u})}{\partial {\mathbf {\mathbf {u}}}}) \cdot
diag(\frac{\partial g(f(\mathbf {u}))}{\partial f(\mathbf {u})}) = diag(\frac{\partial f(\mathbf {u})}{\partial {\mathbf {\mathbf {u}}}} \circ  \frac{\partial g(f(\mathbf {u}))}{\partial f(\mathbf {u})}) 
$

$
\frac{\partial g(f((\mathbf {Au})^\mathbf{T}))}{\partial {\mathbf {u}}} = 
\frac{\partial f((\mathbf {Au})^\mathbf{T})}{\partial {\mathbf {u}}}  \cdot \frac{\partial g(f((\mathbf {Au})^\mathbf{T}))}{\partial f(\mathbf {Au})} = 
\mathbf A^\mathbf{T} \cdot diag(\frac{\partial f(\mathbf {v})}{\partial {\mathbf {\mathbf {v}}}} \circ  \frac{\partial g(f(\mathbf {v}))}{\partial f(\mathbf {v})}) 
$

其中$\mathbf v = \mathbf{Au}$，$\circ $是[哈达玛积](https://zh.wikipedia.org/wiki/%E9%98%BF%E9%81%94%E7%91%AA%E4%B9%98%E7%A9%8D_(%E7%9F%A9%E9%99%A3))，表示两个向量或矩阵的各个分量分别相乘。

而且对角矩阵还有对称的性质，不难得到。

$
diag(\mathbf {v}) \cdot \mathbf {u}  =   \mathbf {v} \circ \mathbf {u} = \mathbf {u} \circ \mathbf {v} 
$

$
\mathbf {u}^\mathbf{T} \cdot diag(\mathbf {v}) = \mathbf {u}^\mathbf{T} \circ \mathbf {v}^\mathbf{T} = \mathbf {v}^\mathbf{T} \circ  \mathbf {u}^\mathbf{T}  =  (\mathbf {v} \circ  \mathbf {u})^\mathbf{T} =  (\mathbf {u} \circ  \mathbf {v})^\mathbf{T}
$

$
\mathbf {A} \cdot diag(\mathbf {v})  =  \mathbf {A} \circ v^\mathbf{T}  = v^\mathbf{T}  \circ  \mathbf {A} 
$

于是，公式还可以进一步简化，最终可以得到如下公式。

$
\frac{\partial f((\mathbf {Au})^\mathbf{T})}{\partial {\mathbf {u}}} = 
\mathbf A^\mathbf{T} \cdot diag(\frac{\partial f(\mathbf {Au})}{\partial \mathbf {Au}})  =      \mathbf A^\mathbf{T} \circ (\frac{\partial f(\mathbf {Au})}{\partial \mathbf {Au}})^\mathbf{T} =     ( \mathbf A \circ \frac{\partial f(\mathbf {Au})}{\partial \mathbf {Au}})^\mathbf{T} 
$

$
\frac{\partial g(f(\mathbf {u}^\mathbf{T}))}{\partial {\mathbf {\mathbf {u}}}} = 
diag(\frac{\partial f(\mathbf {u})}{\partial {\mathbf {\mathbf {u}}}} \circ  \frac{\partial g(f(\mathbf {u}))}{\partial f(\mathbf {u})}) 
$

$
\frac{\partial g(f((\mathbf {Au})^\mathbf{T}))}{\partial {\mathbf {u}}} = 
\mathbf A^\mathbf{T} \cdot diag(\frac{\partial f(\mathbf {v})}{\partial {\mathbf {\mathbf {v}}}} \circ  \frac{\partial g(f(\mathbf {v}))}{\partial f(\mathbf {v})}) =  (\mathbf A \circ \frac{\partial f(\mathbf {v})}{\partial {\mathbf {\mathbf {v}}}} \circ \frac{\partial g(f(\mathbf {v}))}{\partial f(\mathbf {v})})^\mathbf{T}
$

其中$\mathbf v = \mathbf{Au}$

下面看几个实际的例子。

$\frac{\mathbf{d}\log(\mathbf {u}^\mathbf{T})}{\mathbf{d}\mathbf {u}} =diag(\frac 1 {\mathbf {u}})
$

$\frac{\mathbf{d}\log((\mathbf {A}\mathbf {u})^\mathbf{T})}{\mathbf{d}\mathbf {u}} = 
\frac{\mathbf{d}(\mathbf v)^\mathbf{T}}{\mathbf{d}\mathbf {u}} \cdot \frac {\mathbf{d}\log(v^\mathbf{T})} {\mathbf{d} v} = 
\mathbf {A}^\mathbf{T} \cdot diag(\frac  1 {\mathbf  v}) = (\mathbf {A} \cdot \frac  1 {\mathbf v})^\mathbf{T} 
$

其中$$\frac 1 {\mathbf {u}} = \begin{bmatrix} \frac 1 {u_1} \\ \frac 1 {u_2} \\ \vdots \\ \frac 1 {u_n} \end{bmatrix}$$，$\mathbf v = \mathbf{Au}$，$$\frac 1 {\mathbf {v}} = \begin{bmatrix} \frac 1 {v_1} \\ \frac 1 {v_2} \\ \vdots \\ \frac 1 {v_n} \end{bmatrix}$$

