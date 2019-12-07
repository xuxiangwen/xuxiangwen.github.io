---
title: 线性映射和线性变换
categories: linear-algebra
date: 2019-12-05
---
在线性代数中，线性映射（linear mapping）和线性变换（linear transformation）经常被提到。线性映射指从一个向量空间$$\mathbf V$$到另一个向量空间$$\mathbf W$$的映射且保持加法运算和数量乘法运算，而线性变换是线性空间$$\mathbf V$$到其自身的线性映射，是一种特殊的线性映射。

通俗来说，线性映射把一个坐标系中的点，映射到另外一个坐标系中的点，比如：阳光下物体的影子，就是把三维的物体映射到二维的平面上。而线性变换是在同一个坐标系中完成的。比如：二维平面中，对一个图形，进行旋转，缩放。

 ![File:Eigenvectors.gif](/assets/images/Eigenvectors-1575459117113.gif) 

### 定义

设 $$\mathbf V，\mathbf W $$为两个向量空间， 如果$$f:\mathbf V \rightarrow \mathbf W$$满足

- 任意$$ \mathbf{\alpha} \in \mathbf V，$$则$$ f(\mathbf{\alpha}) \in \mathbf W $$ 
- 加法：任意向量$$ \mathbf{\alpha_1},\mathbf{\alpha_2} \in \mathbf V $$，则 $$f(\mathbf{\alpha_1}+\mathbf{\alpha_2}) = f(\mathbf{\alpha_1}) + f(\mathbf{\alpha_2})$$ 
- 数乘：任意向量 $$\mathbf{\alpha} \in \mathbf V $$，则$$ f(k\mathbf{\alpha}) = kf(\mathbf{\alpha})$$ 

则称$$f$$为从线性空间$$\mathbf V$$到线性空间$$\mathbf W $$的**线性映射**。如果$$\mathbf V$$和$$\mathbf W$$是同一个线性空间，则称$$f$$为**线性变换**，线性映射和线性变换很类似，本质相同。

线性映射可以用矩阵表示，这也是矩阵最重要的意义之一。方式如下：

$$

\mathbf A \cdot \mathbf{\alpha} = \mathbf{\beta}

$$

其中$$f = \mathbf A， \mathbf{\alpha} \in \mathbf V， \mathbf {\beta} \in \mathbf W  $$。为了加深理解，下面看最简单的线性变换：旋转，缩放以及正交化。

### 旋转

在同一向量空间，最基本的线性变换之一是旋转。在二维空间，如下矩阵$$\mathbf A$$将会把向量进行逆时针旋转$$\theta $$。

$$

\mathbf A = 
\begin{bmatrix} 
\cos {(\theta)} & -\sin {(\theta)} \\
\sin {(\theta)} & \cos {(\theta)} 
\end{bmatrix} = \begin{bmatrix} \mathbf {a_1}   &  \mathbf {a_2} \end{bmatrix}

$$

其中$\mathbf {a_1} = \begin{bmatrix} 
\cos {(\theta)}  \\
\sin {(\theta)} 
\end{bmatrix} ，
\mathbf {a_2} = 
\begin{bmatrix} 
-\sin{(\theta)}  \\
\cos{(\theta)} 
\end{bmatrix} 
$
如下图所见，向量$$\mathbf {a_1}$$是一个单位向量，和$$\mathbf X$$轴的角度是$$\theta $$，向量$$\mathbf {a_2}$$也是一个单位向量，和$$\mathbf {a_1}$$刚好垂直。

![image-20191113134724199](/assets/images/image-20191113134724199-1575459117113.png)

上图中$$\theta = 30^{\circ}$$，$$\alpha$$和$$\mathbf X$$ 轴的角度$$\phi=45^{\circ}$$，经过线性变换后，$$\beta $$和$$\mathbf X $$轴的角度是$$75^{\circ}$$，也就是说，矩阵正好把向量逆时针旋转了$$ 30^{\circ}$$。

上面的解释或许还是有些抽象，用坐标轴变换来解释旋转会形象的多。

$$

\mathbf{\beta} = \mathbf A \cdot \mathbf{\alpha} = \mathbf {a_1} \alpha_1 + \mathbf {a_2} \alpha_2

$$

   - 把$$\mathbf {a_1}$$和$$\mathbf {a_2}$$看成是新的坐标轴，和标准坐标轴相比，这个坐标轴逆时针旋转了$$\theta $$。
   - 向量$$\mathbf {\beta}$$在新坐标轴下的坐标是$$\begin{bmatrix} 
     \alpha_1 \\
     \alpha_2 
     \end{bmatrix} $$
   - $$\alpha$$和$$X$$轴的角度是$$\phi$$，可以得出向量$$\mathbf {\beta}$$和$$\mathbf {a_1}$$(新$$X$$轴)的角度必然也是$$\phi$$，则向量$$\mathbf {\beta}$$和$$X$$轴的角度是 $$\phi + \theta $$ 。就这样看上去，矩阵$$ \mathbf{A} $$正好把向量$$\mathbf{\alpha}$$逆时针旋转了$$ \theta$$。

同理，很容易把上述方法推广到$$n$$维: 

$$

\mathbf{\beta} = \mathbf A \cdot \mathbf{\alpha} = \mathbf {a_1} \alpha_1 + \mathbf {a_2} \alpha_2 + \cdots \mathbf {a_n} \alpha_n

$$

- 把$$\mathbf {a_1}, \mathbf {a_2}, \cdots, \mathbf {a_n}$$看成是新的坐标轴。
 - 向量$$\mathbf {\beta}$$在新坐标轴下的坐标是$$\begin{bmatrix} 
   \alpha_1 \\
    \alpha_2 \\
    \vdots    \\
    \alpha_n
    \end{bmatrix} $$
- 即使是高维空间，不难得出，**向量$$\mathbf {\beta}$$和$$\mathbf {\alpha}$$之间旋转的角度，等于新旧坐标轴之间的旋转角度**。

本小节中$$\mathbf A$$是一个方阵，其各个列向量是单位向量，且各个列向量之间相互垂直（内积为$$0$$），线性代数中称这样的矩阵为[正交矩阵](https://zh.wikipedia.org/wiki/%E6%AD%A3%E4%BA%A4%E7%9F%A9%E9%98%B5)，而正交矩阵中的向量构成的`基`，称之为`正交基`。正交矩阵最有趣的特性就是旋转，但不改变向量的长度和向量之间的关系。比如：两个向量在原向量空间中，夹角是$$30^{\circ}$$，经过正交矩阵变换后，在新的向量空间，它们的夹角还是$$30^{\circ}$$。

附[代码](https://nbviewer.jupyter.org/github/xuxiangwen/xuxiangwen.github.io/blob/master/_notes/05-ai/50-my-course/machine_learning/c0002.ipynb#旋转)。

### 缩放

在二维空间，下面的矩阵会对向量各个分量进行拉伸和缩放。

$$

\mathbf A = 
\begin{bmatrix} 
s_1 & 0 \\
0 & s_2
\end{bmatrix}

$$

$$

\mathbf{\beta} = 
\mathbf A \cdot \mathbf{\alpha} = 
\begin{bmatrix} 
s_1 & 0 \\
0 & s_2
\end{bmatrix} \cdot \begin{bmatrix} \alpha_1 \\ \alpha_2 \end{bmatrix} = 
\begin{bmatrix} s_1\alpha_1 \\ s_2\alpha_2 \end{bmatrix}

$$

下图中$$\mathbf A = 
\begin{bmatrix} 
2 & 0 \\
0 & 0.5
\end{bmatrix}$$，对圆进行了缩放：$$\mathbf x $$轴$$2$$倍，$$\mathbf y$$轴$$0.5$$倍。

![image-20191114131858572](/assets/images/image-20191114131858572-1575459117113.png)

同样推广到$$n$$维空间。

$$

\mathbf A = 
\begin{bmatrix} 
s_1 & 0 & \cdots & 0 \\
0 & s_2 & \cdots & 0  \\
0 & 0 & \ddots & 0  \\
0 & 0 & 0 & s_n  \\
\end{bmatrix}

$$

上面矩阵的对角线不为0，其他都为0，这样的矩阵称之为**对角矩阵（ diagonal matrix ）**，它的对象线的数对向量的各个分量进行拉伸和缩放。对角矩阵的另外一种更加简化的表达是：

$$

\mathbf A = diag(s_1, s_2, \cdots, s_n)

$$

或者

$$

\mathbf A = diag(\mathbf s)  

$$

其中$$\mathbf s = \begin{bmatrix} s_1 \\ s_2 \\ \vdots \\ s_n \end{bmatrix}$$

附[代码](https://nbviewer.jupyter.org/github/xuxiangwen/xuxiangwen.github.io/blob/master/_notes/05-ai/50-my-course/machine_learning/c0002.ipynb#缩放)。

### 旋转+缩放

正交矩阵带来了旋转，对角矩阵进行了缩放，而旋转，缩放都是一种简单运动，复杂一点的运动可以组合多个旋转，缩放，由此可以把线性映射（变换）理解成一种组合运动。

下图中，对圆先进行缩放：$$\mathbf x $$轴$$2$$倍，$$\mathbf y$$轴$$0.5$$倍，然后再进行旋转$$30^{\circ} $$。

![image-20191114134924766](/assets/images/image-20191114134924766-1575459117113.png)

蓝色的圆是原图，绿色的椭圆是缩放后的，红色的椭圆是绿色椭圆旋转后的样子。$$\mathbf {a_1}, \mathbf {a_2}$$是两种变换叠加后矩阵的列向量。可以这么理解，如果以它们为坐标轴，红色的椭圆就是圆。

所用的两个矩阵分别是：

$$

\mathbf {A_1} = 
\begin{bmatrix} 
2 & 0 \\
0 & 0.5
\end{bmatrix}，\mathbf {A_2} = 
\begin{bmatrix} 
\frac {\sqrt 3} 2 & -\frac 1 2 \\
\frac 1 2 & \frac {\sqrt 3} 2
\end{bmatrix} \\
\mathbf A = \mathbf {A_2} \cdot \mathbf {A_1} = \begin{bmatrix} 
1.732 & -0.25 \\
1 & 0.433 
\end{bmatrix}

$$

附[代码](https://nbviewer.jupyter.org/github/xuxiangwen/xuxiangwen.github.io/blob/master/_notes/05-ai/50-my-course/machine_learning/c0002.ipynb#缩放+旋转)。

### 正交化

一个平行四边形，通过改变角度，可以很容易变成一个长方形。与此类似，[正交化](https://zh.wikipedia.org/wiki/%E6%AD%A3%E4%BA%A4%E5%8C%96)是指把一组（线性无关）的向量经过线性变换后，使得各个向量之间相互垂直（内积为0），然后再对向量进行缩放，使得每个向量成为单位向量。容易想象，在一个二维平面，任意两个向量（不共线），首先通过变换使得两个向量垂直，然后进行缩放，可以把它们变成正交矩阵。

下图中，$$\mathbf {v_2^{'}}$$是$$
\mathbf {v_2}$$在$$\mathbf {v_1}$$上的投影，$$\mathbf {v_2} - \mathbf {v_2^{'}}$$就可以得到垂直于$$\mathbf {v_1}$$的向量$$\mathbf {\beta_2}$$。

![image-20191121102923460](/assets/images/image-20191121102923460-1575459117113.png)

公式表达如下：

$$

\begin{align}
\mathbf {\beta_1} &= \mathbf {v_1}       \\
\mathbf {\beta_2} &= \mathbf {v_2} - (\mathbf {v_2} \cdot \frac {\mathbf {\beta_1}}  {\| \mathbf {\beta_1}\|} ) \frac {\mathbf {\beta_1}}  {\| \mathbf {\beta_1}\|} 
\end{align} \\

$$

然后进行缩放：

$$

\mathbf {\eta_1} =  \frac {\mathbf {\beta_1}}  {\| \mathbf {\beta_1}\|}  \\
\mathbf {\eta_2} =  \frac {\mathbf {\beta_2}}  {\| \mathbf {\beta_2}\|}

$$

以上方法，可以推广到$$n$$维，称之为[格拉姆-施密特正交化](https://zh.wikipedia.org/wiki/%E6%A0%BC%E6%8B%89%E5%A7%86-%E6%96%BD%E5%AF%86%E7%89%B9%E6%AD%A3%E4%BA%A4%E5%8C%96)。

 ![img](/assets/images/300px-GSO-1575459117114.png) 

$$

\begin{align}
\mathbf {V} &= \begin{bmatrix} \mathbf {v_1} & \mathbf {v_2} & \cdots & \mathbf {v_n} \end{bmatrix} \\
\mathbf {\beta_1} &= \mathbf {v_1}     & \mathbf {\eta_1} =  \frac {\mathbf {\beta_1}}  {\| \mathbf {\beta_1}\|}  \\
\mathbf {\beta_2} &= \mathbf {v_2} - (\mathbf {v_2} \cdot \mathbf {\eta_1}) \mathbf {\eta_1} & \mathbf {\eta_2} =  \frac {\mathbf {\beta_2}}  {\| \mathbf {\beta_2}\|}  \\
\mathbf {\beta_3} &= \mathbf {v_3} - (\mathbf {v_3} \cdot \mathbf {\eta_1}) \mathbf {\eta_1} - (\mathbf {v_3} \cdot \mathbf {\eta_2}) \mathbf {\eta_2}   & \mathbf {\eta_2} =  \frac {\mathbf {\beta_3}}  {\| \mathbf {\beta_3}\|}  \\
\vdots \\
\mathbf {\beta_n} &= \mathbf {v_n} - \sum_{i=1}^{n-1} (\mathbf {v_n} \cdot \mathbf {\eta_i}) \mathbf {\eta_i} & \mathbf {\eta_n} =  \frac {\mathbf {\beta_n}}  {\| \mathbf {\beta_n}\|}  
\end{align}

$$

其中$$\begin{bmatrix} \mathbf {\eta_1} & \mathbf {\eta_2} & \cdots & \mathbf {\eta_n} \end{bmatrix}$$就是经过变换后的正交矩阵。

通过上面的分析，可以得出：一组（线性无关）的向量总可以通过线性变换变成正交矩阵。

> 线性无关是指一组向量中，任意向量无法通过其他向量线性组合所表示，反之称之为线性相关。比如：三角形的任意一边所表示向量可由其他两边向量加法或减法而得，这说明这三个向量是线性相关的。而单位矩阵中，各个向量都无法由其他的向量线性组合而成，所以是线性无关的。

附[代码](https://nbviewer.jupyter.org/github/xuxiangwen/xuxiangwen.github.io/blob/master/_notes/05-ai/50-my-course/machine_learning/c0002.ipynb#正交化)。

### 内积和投影

还可以从内积角度来理解线性映射。    

$$

\begin{align} 
\mathbf{\beta} &= \mathbf A \cdot \mathbf{\alpha}  \\
\mathbf{\beta} &= 
\begin{bmatrix} 
\mathbf {a_1^T} \\ 
\mathbf {a_2^T} \\
\vdots \\
\mathbf {a_m^T} 
\end{bmatrix} \cdot  \mathbf{\alpha} \\
\mathbf{\beta} &= 
\begin{bmatrix} 
\mathbf {a_1^T}\cdot  \mathbf{\alpha} \\ 
\mathbf {a_2^T}\cdot  \mathbf{\alpha} \\
\vdots \\
\mathbf {a_m^T}\cdot  \mathbf{\alpha} 
\end{bmatrix} 
\end{align}

$$

通过上面的推导可以看出，$$\mathbf \beta$$可以理解为向量$$\mathbf \alpha$$和$$\mathbf  A$$各个行向量的内积。线性映射的过程，就是把$$\mathbf \alpha$$从$$n$$维空间映射到$$m$$维空间的过程。

当$$\mathbf {a_1}, \mathbf {a_2}, \cdots, \mathbf {a_m}$$是单位向量时，**$$\mathbf \beta$$是向量$$\mathbf \alpha$$ 在$$\mathbf  A$$各个行向量上的投影**，即以行向量为基的坐标系上的坐标。

### 参考

- [百度百科：线性变换](https://baike.baidu.com/item/%E7%BA%BF%E6%80%A7%E5%8F%98%E6%8D%A2)
- [回顾线性空间](https://scientificrat.com/2017/10/11/%E5%9B%9E%E9%A1%BE%E7%BA%BF%E6%80%A7%E7%A9%BA%E9%97%B4/)
