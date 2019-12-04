---
title: 点到平面的距离
categories: linear-algebra
date: 2019-12-04
---
上文中说到，$$\mathbf w \cdot \mathbf x = 0$$，表示一个过原点，且垂直于$$\mathbf w$$的平面方程。而对于空间中任意平面，其平面方程为：$$ \mathbf w  \cdot \mathbf x + b = 0$$，该平面垂直于$$\mathbf w$$，但不一定过原点。

![image-20191111144652944](/assets/images/image-20191111144652944-1575459054585.png)

- 如果是二维空间，则表示是一个直线方程。比如：

  直线$$2x+3y+5=0$$，即$$\begin{bmatrix} 2 \\ 3 \end{bmatrix} \cdot \begin{bmatrix} x \\ y  \end{bmatrix} + 5 = 0$$

- 如果是三维空间, 是一个平面. 如果大于3维空间，则是一个超平面。

空间任意一点$$x$$到平面的距离是:  

$$

\gamma = \frac 1 {\|\mathbf w\|} (\mathbf w \cdot \mathbf x + b)

$$

- $$ \gamma >0 $$，表示$$\mathbf x$$在平面上方
- $$\gamma<0$$，表示$$\mathbf x$$在平面下方

### 证明

假设点$$\mathbf {x_0} $$是指点$$ \mathbf x  $$在超平面上的投影点，即$$\vec {x_0x}$$ 平行于$$ \mathbf w$$。

$$

\mathbf x - \mathbf{x_0} = \gamma  \frac {\mathbf w} {\|\mathbf w\|}
 \\
 \mathbf w \cdot (\mathbf  x- \mathbf{x_0}) = \mathbf w \cdot \gamma  \frac {\mathbf w} {\|\mathbf  w\|}

$$

 由于$$ \mathbf w \cdot \mathbf  {x_0} + b = 0  $$, 即 $$ \mathbf w  \cdot \mathbf {x_0}  = -b  $$, 上面的公式可以变成

$$

\gamma = \frac 1 {\|\mathbf  w\|}(\mathbf  w \cdot \mathbf  x + b)

$$

### 意义

机器学习的二分类问题，从几何角度来看，可以看成是找到一个平面（甚至曲面）把两个类别分开的事情。如果样本到平面的距离越大，则认为分类的效果越好，而这也是学习点到平面距离的意义。在后面学习`支持向量机`（support vector machine）时，尤其会用到这个概念。

 ![SVM Lines](/assets/images/DYoJdfp-1575459054585.jpg) 

 上图中，虽然都很能正确分类，由于蓝线距离样本距离明更大，所以蓝线比红线分类效果要好。

### 参考

- [支持向量机通俗导论（理解SVM的三层境界）](https://blog.csdn.net/v_JULY_v/article/details/7624837)