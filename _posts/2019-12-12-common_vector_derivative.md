---
title: 常用向量导数公式
categories: linear-algebra
date: 2019-12-12
---
下面对常用的向量导数公式进行汇总，在实际工作总，可以方便直接使用。

#### 基本公式

使用这些公式可以推导出其它公式。

$$

\begin{align}
&\frac{\partial \mathbf {w}^\mathbf{T} }{\partial \mathbf {w} } = \mathbf{I_n}
\\ \\
&\frac{\partial \mathbf {u} }{\partial \mathbf {w} } = 
\begin{bmatrix}
\frac{\partial  {u_1} }{\partial {w_1} } \\
\frac{\partial  {u_2} }{\partial {w_2} } \\
\vdots \\
\frac{\partial  {u_n} }{\partial {w_n} }
\end{bmatrix}
\\ \\
&\frac{\partial \mathbf {u}^\mathbf{T}\mathbf {v} }{\partial \mathbf {w} } =  \frac{\partial \mathbf {u}^\mathbf{T} }{\partial \mathbf {w} } \cdot \mathbf {v} + \frac{\partial \mathbf {v}^\mathbf{T} }{\partial \mathbf {w} } \cdot \mathbf {u}
\\ \\
&\mathbf {A} \cdot diag(\mathbf {w})  =  \mathbf {A} \circ \mathbf {w}^\mathbf{T}  = \mathbf {w}^\mathbf{T}  \circ  \mathbf {A} 
\\ \\
&\frac {\partial f(\mathbf {w}^{\mathbf {T} })} {\partial \mathbf {w} } = diag(\frac {\partial f(\mathbf {w})} {\partial \mathbf {w} }) 
\\ \\
&\frac{\partial g(f(\mathbf {w}^\mathbf{T}))}{\partial \mathbf {w} } =   \frac{\partial f(\mathbf {w}^\mathbf{T})}{\partial \mathbf {w} } \cdot  \frac{\partial g(f(\mathbf {w}^\mathbf{T}))}{\partial g(\mathbf {w})} = diag(\frac{\partial f(\mathbf {w})}{\partial {\mathbf {\mathbf {w}}}}) \circ  diag(\frac{\partial g(f(\mathbf {w}))}{\partial f(\mathbf {w})}) 
\end{align}

$$

#### 通用公式

从基本公式衍生而来。

$$

\begin{align}
& \frac{\partial \mathbf {w}^\mathbf{T}\mathbf {w} }{\partial \mathbf {w} } = 2\mathbf {w}
\\ \\
& \frac{\partial (\mathbf{A}\mathbf {w})^\mathbf{T} }{\partial \mathbf {w} } =  \mathbf{A}^\mathbf{T} 
\\ \\
& \frac{\partial \mathbf {w}^\mathbf{T} \mathbf{B} \mathbf {w} } {\partial \mathbf {w} } =  (\mathbf{B} + \mathbf{B}^\mathbf{T})\cdot \mathbf {w} 
\\ \\ 
& \frac{\partial f((\mathbf {Au})^\mathbf{T})}{\partial {\mathbf {u}}}  
 =      \mathbf A^\mathbf{T} \cdot  diag(\frac{\partial f(\mathbf {Au})}{\partial \mathbf {Au}}) =      \mathbf A^\mathbf{T} \circ (\frac{\partial f(\mathbf {Au})}{\partial \mathbf {Au}})^\mathbf{T}
 \\  \\
& \frac{\partial g(f((\mathbf {Au})^\mathbf{T}))}{\partial {\mathbf {u}}} = \mathbf A^\mathbf{T} \cdot diag(\frac{\partial f(\mathbf {Au})}{\partial {\mathbf {\mathbf {Au}}}}) \cdot diag(\frac{\partial g(f(\mathbf {Au}))}{\partial f(\mathbf {Au})}) = 
\mathbf A^\mathbf{T} \circ （\frac{\partial f(\mathbf {Au})}{\partial {\mathbf {\mathbf {Au}}}})^\mathbf{T}  \circ  (\frac{\partial g(f(\mathbf {Au}))}{\partial f(\mathbf {Au})})^\mathbf{T}   
\end{align}

$$

#### 实际公式

在通用公式基础上，所用函数都是具体的。

$$

\begin{align}
& \frac{\mathbf{d}\log(\mathbf {u}^\mathbf{T})}{\mathbf{d}\mathbf {u}} =diag(\frac 1 {\mathbf {u}})
\\ \\
& \frac{\mathbf{d}\log((\mathbf {A}\mathbf {u})^\mathbf{T})}{\mathbf{d}\mathbf {u}} = \mathbf {A}^\mathbf{T} \cdot diag(\frac  1 {\mathbf  {Au}}) = \mathbf {A}^\mathbf{T} \circ (\frac  1 {\mathbf  Au})^\mathbf{T}
\end{align}

$$

