---
title: LaTex速查
categories: others
date: 2020-08-18
---

**LaTeX**（/ˈlɑːtɛks/）是一种基于[TEX](https://zh.wikipedia.org/wiki/TeX)的排版系统，由美国计算机科学家[莱斯利·兰伯特](https://zh.wikipedia.org/wiki/莱斯利·兰伯特)在20世纪80年代初期开发，利用这种格式系统的处理，即使用户没有排版和程序设计的知识也可以充分发挥由TEX所提供的强大功能，不必一一亲自去设计或校对，能在几天，甚至几小时内生成很多具有书籍质量的印刷品。

本文汇总了常用的LaTex符号和公式，以便速查。

## 常用

| 符号   | LaTex     | 描述         |
| :-------- | :------------ | :----------- |
| $\leq$    | \leq          | 小于等于     |
| $\geq$    | \geq | 大于等于     |
| $\neq$    | \neq | 不等于       |
| $\approx$ | \approx | 约等于       |
| $X  \sim  \mathcal N(\mu,\sigma^2)$ | X  \sim  \mathcal N(\mu,\sigma^2) | 符合正态分布 |
| $\hat{A}$ | \hat {A}      | 估计值       |
| $X \in R^{n \times m}$ | X \in R^{n \times m} | 属于 |
| $  u^\mathrm{T} $  |  u^T | 矩阵转置 |
| $\mathrm{d}u $ | \mathrm{d}u  | 微分 |
| $\frac 1 m $ | \frac 1 m  | 分数 |
| $\frac {\partial u^T} {\partial u} $ | \frac {\partial u^T} {\partial u} | 偏导数 |
| $\nabla{w} $  | \nabla{w} | 梯度 |
| $\prod\limits_i^m x_i$ | \prod\limits_i^m x_i | 连乘 |
| $\sum\limits_i^m$ | \sum\limits_i^m  | 累加 |
| $\lVert {w} \rVert _{2} = w^\mathrm{T}w $ |  \lVert {w} \rVert _{2} = w^\mathrm{T}w |  |
| $\square$ | \square | 正方形 |
| $\triangle$ | \triangle | 三角形 |

## 希腊字母

| 符号      | LaTex   |
| :-------- | :------ |
| $\varphi$ | \varphi |
| $\phi$    | \phi    |
| $\Phi$    | \Phi    |

## 集合操作 

| 符号         | LaTex      | 描述     |
| :----------- | :--------- | :------- |
| $\cup$       | \cup       | 并集     |
| $\in$        | \in        | 属于     |
| $\notin$     | \notin     | 不属于   |
| $\subset$    | \subset    | 被真包含 |
| $\subseteq $ | \subseteq  | 被包含   |
| $\supset$    | \subset    | 真包含   |
| $\supseteq $ | \subseteq  | 包含     |
| $\mid$       | \mid       |          |
| $\mathbb{R}$ | \mathbb{R} | 实数     |
| $\mathbb{Z}$ | \mathbb{Z} | 实数     |
| $\mathbb{N}$ | \mathbb{N} | 实数     |

## 其它

### 对齐+公式编号

$$
\begin{align}
y &= x + 5 \\
&= 3 + 5 \\
&= 8  \tag 1
\end{align}
$$

~~~latex
\begin{align}
y &= x + 5 \\
&= 3 + 5 \\
&= 8  \tag 1
\end{align}
~~~

### 括号

#### 大括号

$$
BP = \begin{equation}  
\left\{  
\begin{array}{lcl}  
 1        &  & if\ c>r \\  
 e^{(1-r/c)} &  & if\ c<=r  
\end{array}  
\right.
\end{equation}
$$

~~~latex
BP = \begin{equation}  
\left\{  
\begin{array}{lcl}  
 1        &  & if\ c>r \\  
 e^{(1-r/c)} &  & if\ c<=r  
\end{array}  
\right.  
\end{equation}   
~~~

#### 小括号

$$
\left( \frac{a}{b} \right)
$$

~~~latex
\left( \frac{a}{b} \right)
~~~

#### 中括号 

$$
\left[ \frac{a}{b} \right]
$$

~~~latex
\left[ \frac{a}{b} \right]
~~~

#### 下括号和上括号

$$
\underbrace{\mathbf{A}}_{n\times n}{\mathbf{v}} = \underbrace{\lambda}_{eigenvalue} \overbrace{\mathbf{v}}^{eigenvector}
$$

~~~latex
\underbrace{\mathbf{A}}_{n\times n}{\mathbf{v}} = \underbrace{\lambda}_{eigenvalue} \overbrace{\mathbf{v}}^{eigenvector}
~~~

### 箭头

| 符号         | LaTex      | 描述     |
| :----------- | :--------- | :------- |
| $\uparrow	          $ | \uparrow	             |        |
| $\downarrow	        $ | \downarrow	           |        |
| $\Uparrow	          $ | \Uparrow	             |        |
| $\Downarrow	        $ | \Downarrow	           |        |
| $\updownarrow	      $ | \updownarrow	         |        |
| $\Updownarrow	      $ | \Updownarrow	         |        |
| $\rightarrow	      $ | \rightarrow	           |        |
| $\leftarrow	        $ | \leftarrow	           |        |
| $\Rightarrow	      $ | \Rightarrow	           |        |
| $\Leftarrow	        $ | \Leftarrow	           |        |
| $\leftrightarrow	  $ | \leftrightarrow	       |        |
| $\Leftrightarrow	  $ | \Leftrightarrow	       |        |
| $\longrightarrow	  $ | \longrightarrow	       |        |
| $\longleftarrow	    $ | \longleftarrow	       |        |
| $\Longrightarrow	  $ | \Longrightarrow	       |        |
| $\Longleftarrow	    $ | \Longleftarrow	       |        |
| $\longleftrightarrow$ | \longleftrightarrow	   |        |
| $\Longleftrightarrow$ | \Longleftrightarrow	   |        |



### Excel转化成markdown Table

[Copy Table in Excel and Paste as a Markdown Table](https://thisdavej.com/copy-table-in-excel-and-paste-as-a-markdown-table/)

## 参考

- [Markdown备忘录](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
- [MarkDown](https://sourceforge.net/p/ipython/discussion/markdown_syntax)
- [Math IM](http://mathim.com/static/chatprimer.html)
- [LaTex数学公式 ](http://blog.163.com/goldman2000@126/blog/static/167296895201221242646561/)
- [LaTex/Mathematics](https://en.wikibooks.org/wiki/LaTex/Mathematics)
- [LaTex中导数、极限、求和、积分 ](http://blog.csdn.net/foreverdengwei/article/details/7665035)
- [LaTex大括号公式和一般括号总结](https://blog.csdn.net/miao0967020148/article/details/78712811)
- [$T_EX $ commands available in MathJax](https://www.emath.ac.cn/download/doc/mathTeX.pdf) : 非常详细
- [MathJax在线](https://kexue.fm/latex.html)

