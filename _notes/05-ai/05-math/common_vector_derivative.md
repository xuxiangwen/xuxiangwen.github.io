---
title: 常用向量导数公式
categories: linear-algebra
date: 2019-12-12
---
下面对常用的向量导数公式进行汇总，在实际工作总，可以方便直接使用。

## 基本原则

使用这些公式可以推导出其它公式。

$$
\begin{align}
&\frac{\partial  {w}^{T} }{\partial  {w} } = {I_n}
\\ \\
&\frac{\partial  {u} }{\partial  {w} } = 
\begin{bmatrix}
\frac{\partial  {u_1} }{\partial {w_1} } \\
\frac{\partial  {u_2} }{\partial {w_2} } \\
\vdots \\
\frac{\partial  {u_n} }{\partial {w_n} }
\end{bmatrix}
\\ \\
&\frac{\partial  {u}^{T} {v} }{\partial  {w} } =  \frac{\partial  {u}^{T} }{\partial  {w} } \cdot  {v} + \frac{\partial  {v}^{T} }{\partial  {w} } \cdot  {u}
\\ \\
& {A} \cdot diag( {w})  =   {A} \circ  {w}^{T}  =  {w}^{T}  \circ   {A} 
\\ \\
&\frac {\partial f( {w}^{ {T} })} {\partial  {w} } = diag(\frac {\partial f( {w})} {\partial  {w} }) 
\\ \\
&\frac{\partial g(f( {w}^{T}))}{\partial  {w} } =   \frac{\partial f( {w}^{T})}{\partial  {w} } \cdot  \frac{\partial g(f( {w}^{T}))}{\partial g( {w})} = diag(\frac{\partial f( {w})}{\partial { { {w}}}}) \circ  diag(\frac{\partial g(f( {w}))}{\partial f( {w})}) 
\end{align}
$$

## 通用公式

从基本公式衍生而来。

$$
\begin{align}
& \frac{\partial  {w}^{T} {w} }{\partial  {w} } = 2 {w}
\\ \\
& \frac{\partial ({A} {w})^{T} }{\partial  {w} } =  {A}^{T} 
\\ \\
& \frac{\partial  {w}^{T} {B}  {w} } {\partial  {w} } =  ({B} + {B}^{T})\cdot  {w} 
\\ \\ 
& \frac{\partial f(( {Au})^{T})}{\partial { {u}}}  
 =       A^{T} \cdot  diag(\frac{\partial f( {Au})}{\partial  {Au}}) =       A^{T} \circ (\frac{\partial f( {Au})}{\partial  {Au}})^{T}
 \\  \\
& \frac{\partial g(f(( {Au})^{T}))}{\partial { {u}}} =  A^{T} \cdot diag(\frac{\partial f( {Au})}{\partial { { {Au}}}}) \cdot diag(\frac{\partial g(f( {Au}))}{\partial f( {Au})}) = 
 A^{T} \circ （\frac{\partial f( {Au})}{\partial { { {Au}}}})^{T}  \circ  (\frac{\partial g(f( {Au}))}{\partial f( {Au})})^{T}   
\end{align}
$$

## 常用公式

在通用公式基础上，所用函数都是具体的。

### log函数

$$
\begin{align}
& \frac{\partial \log( {u}^{T})}{\partial  {u}} =diag(\frac 1 { {u}})
\\ \\
& \frac{\partial \log(( {A} {u})^{T})}{\partial  {u}} =  {A}^{T} \cdot diag(\frac  1 {  {Au}}) =  {A}^{T} \circ (\frac  1 {  {Au}})^{T}
\end{align}
$$

### sigmoid函数

$$
h(u) = \frac 1 {1+e^{-u}}
$$

导数公式如下：

$$
\begin{align}
& \frac{\partial h(u)^T}{\partial  {u}} =diag(h(u)(1-h(u)))
\\ \\
& \frac{\partial h( {A} {u})^{T}}{\partial  {u}} =  {A}^{T} \cdot diag(h(Au)(1-h(Au))) =  {A}^{T} \circ \left ( h(Au)^{T}  (1-h(Au))^{T} \right )
\\ \\
& \frac{\partial\log h( {A} {u})^{T}}{\partial  {u}} =   {A}^{T} \circ \left ( h(Au)^{T}  (1-h(Au))^{T} \right ) \circ \frac 1 {h(Au)^{T}} = {A}^{T} \circ   (1-h(Au))^{T} 
\end{align}
$$

### softmax函数

$$
\begin{align}
a_i = h(z_i) =   \frac {e^{z_i}}  {\sum_{k=1}^K e^{z_k}}
\end{align}
$$

其中
$$
z = \begin{bmatrix} z_1 \\ z_2 \\ \vdots \\ z_i \\ \vdots \\ z_K \end{bmatrix}, \ 
a = \begin{bmatrix} a_1 \\ a_2 \\ \vdots \\ a_i \\ \vdots \\ a_K \end{bmatrix}
$$
导数公式如下：
$$
\frac{\partial a_j}{\partial  {z_i}} = \begin{equation}  
\left\{  
\begin{array}{lcl}  
 a_i(1-a_i)  &  &  i=j \\  
-a_i a_j &  &  i\neq j  
\end{array}  
\right.
\end{equation}
$$

$$
\frac{\partial a^T}{\partial  {z}} =  diag(a) - a \cdot {a}^{T}
$$

$$
\begin{align}
& \frac{\partial h( {A} {z})^{T}}{\partial  {z}} =  {A}^{T} \cdot \left ( diag(h(Az)) - h(Az) \cdot {h(Az)}^{T} \right )
\end{align}
$$

$$
\begin{align}

\frac{\partial\log h( {A} {z})^{T}}{\partial  {z}} & =   {A}^{T} \cdot \left ( diag(h(Az)) - h(Az) \cdot {h(Az)}^{T} \right ) \circ \frac 1 {h(Az)^{T}} 
\\ & = {A}^{T} \cdot  \left (1-h(Az)d \right ) 
\end{align}
$$

其中$d = \begin{bmatrix} 
1 & 1&  \ldots&  1
\end{bmatrix}
$。

## 历史

- 2020-10-16：添加sigmoid，softmax函数