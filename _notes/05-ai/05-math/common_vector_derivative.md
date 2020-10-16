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


$$
\begin{align}
& \frac{\partial h(u)^T}{\partial  {u}} =diag(h(u)(1-h(u)))
\\ \\
& \frac{\partial h( {A} {u})^{T}}{\partial  {u}} =  {A}^{T} \cdot diag(h(Au)(1-h(Au))) =  {A}^{T} \circ \left ( h(Au)^{T}  (1-h(Au))^{T} \right )
\end{align}
$$


## 历史

- 2020-10-16：添加sigmoid函数