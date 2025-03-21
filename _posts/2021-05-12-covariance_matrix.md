---
# generated from _notes/05-ai/05-math/covariance_matrix.md

title: 理解协方差矩阵
categories: mathematics
date: 2021-05-12
---

协方差矩阵（Covariance Matrix）非常的有用重要，本文介绍了协方差矩阵以及如下几个方面的应用，希望能够帮助大家理解它。

- 正态分布
- 马氏距离
- 主成分分析

## 协方差矩阵

在统计学与概率论中，协方差矩阵的每个元素是各个向量元素之间的协方差，是从标量随机变量到高维度随机向量的自然推广。它的公式如下：

$$

\Sigma = 
\begin{bmatrix}
\sigma(\mathbf {X_1},\mathbf {X_1}) & \sigma(\mathbf {X_1},\mathbf {X_2}) & \cdots & \sigma(\mathbf {X_1},\mathbf {X_d}) \\
\sigma(\mathbf {X_2},\mathbf {X_1}) & \sigma(\mathbf {X_2},\mathbf {X_2}) & \cdots & \sigma(\mathbf {X_2},\mathbf {X_d})  \\
\vdots & \vdots & \ddots & \vdots  \\
\sigma(\mathbf {X_d},\mathbf {X_1}) & \sigma(\mathbf {X_d},\mathbf {X_2}) & \cdots  & \sigma(\mathbf {X_d},\mathbf {X_d})\\
\end{bmatrix}

$$

其中 $$\mathbf X = \left[ \begin{matrix} \mathbf {X_{1}} & \mathbf {X_{2}} &\cdots&\mathbf {X_{d}}\end{matrix}\right]^{\mathbf T}$$，表示$$d$$个随机变量，$$\sigma(\mathbf {X_i},\mathbf {X_j})$$表示协方差，$$\sigma(\mathbf {X_i},\mathbf {X_j})=E[(\mathbf{X_i}-E(\mathbf{X_i})(\mathbf{Y_j}-E(\mathbf{Y_j})]$$。

协方差矩阵还可以用向量的方式来表达，形式如下：

$$

\Sigma = \frac 1 {n-1} \begin{bmatrix} x_1-\mu & x_2-\mu & \cdots & x_n-\mu \end{bmatrix}\begin{bmatrix} x_1-\mu & x_2-\mu & \cdots & x_n-\mu\end{bmatrix}^\mathrm{T}  \tag{1}

$$

其中$$\mathbf X = \begin{bmatrix} x_1 
& x_2 & \cdots & x_n\end{bmatrix}
$$，$n$表示样本的个数， $x_i$表示一个样本，是一个长度为$d$的向量。

## 正态分布

接下来看看协方差在正态分布里面的应用。对于最常用的一元正态分布，我们几何看不到它（协方差）的样子，直到多元正态分布，协方差才姗姗出场。下面先来复习一下一元正态分布。

### 一元正态分布

![正态分布- 维基百科，自由的百科全书](/assets/images/325px-Normal_Distribution_PDF.svg.png)

它的密度函数如下。

$$

f(x) = \frac{1}{\sqrt{2π}\sigma}e^{-\frac{(x-\mu)^2}{2\sigma^{2}}}

$$

> 根据[中心极限定理](https://zh.wikipedia.org/zh-hans/%E4%B8%AD%E5%BF%83%E6%9E%81%E9%99%90%E5%AE%9A%E7%90%86)，任何分布的一系列独立同分布的变量，它们的均值呈正态分布。这时高斯分布运用如此广泛的原因之一。

### 多元正态分布

$d$元正态分布概率密度函数如下：

$$

\begin{align}
f(x) &= \frac{1}{(\sqrt{2π})^{d}\left|\Sigma\right|^\frac{1}{2}}e^{-\frac{ 1}{2} (x\  -\  \mu)^\mathrm{T}\  \Sigma^{-1}\  (x\  -\  \mu)}
\end{align}

$$

其中

-  $$x=\begin{bmatrix} x_1 & x_2 & \cdots & x_d \end{bmatrix}^\mathrm{T} $$，表示一个样本，它是一个长度为$d$的向量。
- $$u =  \begin{bmatrix} \mu_{1}& \mu_{2}&\cdots&\mu_{d}\end{bmatrix}^\mathrm{T}$$，表示随机变量的均值，也是一个长度为$d$的向量。
-  $$\sigma =  \begin{bmatrix} \sigma _{1}& \sigma _{2}&\cdots&\sigma_{d} \end{bmatrix}^\mathrm{T}$$，表示随机变量的方差。
- $$\Sigma$$表示协方差矩阵（Covariance Matrix）。
- $$\Sigma^{-1}$$表示协方差矩阵的逆矩阵
- $\mid \Sigma\mid^{\frac{1}{2}}$表示协方差矩阵的行列式的平方根。

说起来，上面的公式还真的抽象，为了简化，首先看独立的多元正态分布。

#### 独立多元正态分布

如果$d$个随机变量相互独立，根据联合概率密度公式可以得到：

$$

\begin{align}
f(x) &= p(x_{1},x_{2}....x_{d}) 
\\&= p(x_{1})p(x_{2})....p(x_{d}) 
\\&= \frac{1}{(\sqrt{2π})^n\sigma_{1}\sigma_{2}\cdots\sigma_{d}}e^{-\frac{(x_{1}-\mu_{1})^2}{2\sigma_{1}^2}-\frac{(x_{2}-\mu_{2})^2}{2\sigma_{2}^2}\cdots-\frac{(x_{d}-\mu_{d})^2}{2\sigma_{d}^2}}
\end{align}

$$

令$$z^{2} = \frac{(x_{1}-\mu_{1})^2}{\sigma_{1}^2}+\frac{(x_{2}-\mu_{2})^2}{\sigma_{2}^2}\cdots+\frac{(x_{d}-\mu_{d})^2}{\sigma_{d}^2}$$，$$\sigma_{z}= \sigma_{1}\sigma_{2}\cdots\sigma_{d}$$，公式可以简化为：

$$

f(x) = \frac{1}{(\sqrt{2π})^n\sigma_{z}}e^{-\frac{z^2}{2}}  \tag 2

$$

于是可以把$z^{2}$转换成矩阵的形式。

$$

\begin{align}
z^2 &=  \left[ \begin{matrix} x_{1} - \mu_{1}, x_{2} - \mu_{2}, \cdots,x_{d} - \mu_{d}\end{matrix}\right] \left[ \begin{matrix} \frac{1}{\sigma_{1}^2}&0&\cdots&0\\ 0&\frac{1}{\sigma_{2}^2}&\cdots&0\\ \vdots&\vdots&\ddots&\vdots\\ 0&0&\cdots&\frac{1}{\sigma_{d}^2}  \end{matrix}\right]\left[ \begin{matrix} x_{1} - \mu_{1}\\x_{2} - \mu_{2}\\ \vdots \\x_{d} - \mu_{d}\end{matrix}\right]
\end{align}  \tag 3

$$

然后，由于这些变量是相互独立的，不同变量之间的协方差为0，可以得到协方差矩阵和它的逆矩阵。

$$

\Sigma = \left[ \begin{matrix} \sigma_{1}^2&0&\cdots&0\\ 0&\sigma_{2}^2&\cdots&0\\ \vdots&\vdots&\ddots&\vdots\\ 0&0&\cdots&\sigma_{d}^2  \end{matrix}\right] \tag 4

$$

$$

\Sigma^{-1} = \left[ \begin{matrix} \frac{1}{\sigma_{1}^2}&0&\cdots&0\\ 0&\frac{1}{\sigma_{2}^2}&\cdots&0\\ \vdots&\vdots&\ddots&\vdots\\ 0&0&\cdots&\frac{1}{\sigma_{d}^2}  \end{matrix}\right]  \tag 5

$$

由此很容易得到如下公式。

$$

\sigma_{z}= \left|\Sigma\right|^\frac{1}{2} =\sigma_{1}\sigma_{2}.....\sigma_{d}   \tag 6

$$

把公式$(3) - (6)$代入公式 $ （2)$，可以推得：

$$

\begin{align}
f(x) &= \frac{1}{(\sqrt{2π})^n\sigma_{z}}e^{-\frac{z^2}{2}} 
\\&= \frac{1}{(\sqrt{2π})^{d}\left|\Sigma\right|^\frac{1}{2}}e^{-\frac{ 1}{2} (x\  -\  \mu)^\mathrm{T}\  \Sigma^{-1}\  (x\  -\  \mu)}
\end{align}  \tag 7

$$

由此证明完毕，当随机变量相互独立时，公式成立。

#### 非独立多元正态分布

我们知道，协方差矩阵是一个实对称矩阵。而如果对实对称矩阵进行特征值分解，会发现其特征向量矩阵是一个正交矩阵（相关证明详见[正交矩阵](https://eipi10.cn/linear-algebra/2019/12/07/eigenvalue_and_eigenvector/#%E6%AD%A3%E4%BA%A4%E7%9F%A9%E9%98%B5)），也就是：

$$

\mathbf{\Sigma} =  \mathbf{V} \mathbf {\Lambda} \mathbf{V^T} \tag 8

$$

其中$\mathbf V$是正交矩阵，$\mathbf {\Lambda} = diag(\mathbf {\lambda_1}, \mathbf {\lambda_2}, \cdots,  \mathbf {\lambda_d})$，是一个对角矩阵，对角线的值代表特征值。

然后，根据正交矩阵的性质$$ \mathbf{V^T} \mathbf V =1$$，可以对上面公式进行分解，可以得到。

$$

\begin{align}
\mathbf{V^T}\ \mathbf{\Sigma}\ \mathbf{V}  &=  \mathbf {\Lambda}  \\
 \frac 1 {n-1} \mathbf{V^T}\begin{bmatrix} x_1-\mu & x_2-\mu & \cdots & x_n-\mu \end{bmatrix}\begin{bmatrix} x_1-\mu & x_2-\mu & \cdots & x_n-\mu\end{bmatrix}^\mathrm{T} \mathbf{V } &=  \mathbf {\Lambda} \\
 \frac 1 {n-1} \mathbf{V^T}\begin{bmatrix} x_1-\mu & x_2-\mu & \cdots & x_n-\mu \end{bmatrix}  \left(  \mathbf{V^T}   \begin{bmatrix} x_1-\mu & x_2-\mu & \cdots & x_n-\mu \end{bmatrix}  \right)^\mathrm{T} &=  \mathbf {\Lambda} 
\end{align}

$$

再设$$x^{'}_i =\mathbf{V^T} x_i，\mu^{'} = \mathbf{V^T} \mu $$，上式可以简化为：

$$

\begin{align} 
 \frac 1 {n-1} \begin{bmatrix} x_1^{'}-\mu^{'} & x_2^{'}-\mu^{'} & \cdots & x_n^{'}-\mu^{'} \end{bmatrix}      \begin{bmatrix} x_1^{'}-\mu^{'} & x_2^{'}-\mu^{'} & \cdots & x_n^{'}-\mu^{'} \end{bmatrix}  ^\mathrm{T} &=  \mathbf {\Lambda} \\
\end{align}

$$

上面的式子的左边，看起来有点和公式$(1)$非常象，分明它就是对于$$x^{'}$$的协方差矩阵。即：

$$

\begin{align}
 \mathbf{\Sigma}^{'} = \frac 1 {n-1} \begin{bmatrix} x_1^{'}-\mu^{'} & x_2^{'}-\mu^{'} & \cdots & x_n^{'}-\mu^{'} \end{bmatrix}      \begin{bmatrix} x_1^{'}-\mu^{'} & x_2^{'}-\mu^{'} & \cdots & x_n^{'}-\mu^{'} \end{bmatrix}  ^\mathrm{T} &=  \mathbf {\Lambda} \\
\end{align}

$$

观察上面公式，不难发现，$$\mathbf {\Lambda} $$是一个对角矩阵，除了对角线外，其它地方都为0，这说明变量之间相互独立，而这刚好符合独立多元正态分布的条件，于是套用上一章的公式$(7)$，可以得到。

$$

\begin{align}
f(x^{'}) = \frac{1}{(\sqrt{2π})^{d}\left|\Sigma_{n-1}^{'}\right|^\frac{1}{2}}e^{-\frac{ 1}{2} (x^{'}\  -\  \mu^{'})^\mathrm{T}\  {\Sigma^{'}}^{-1}\  (x^{'}\  -\  \mu^{'})}
\end{align}

$$

接下来，把$$x^{'} =\mathbf{V^T} x， \mu^{'} = \mathbf{V^T} \mu $$， $$ \mathbf{\Sigma}^{'}=\mathbf {\Lambda}$$带入上式。

$$

\begin{align}
f(x) = \frac{1}{(\sqrt{2π})^{d}\left|\mathbf {\Lambda}\right|^\frac{1}{2}}e^{-\frac{ 1}{2} (x\  -\  \mu)^\mathrm{T}\ \mathbf{V}  {\mathbf {\Lambda}}^{-1}  \mathbf{V^T}\  (x\  -\  \mu)}  
\end{align}

$$

接着，由于$\mathbf {\Lambda}$是对角矩阵，显然$$\mid \mathbf {\Lambda} \mid = \prod\lambda_i  $$ ，可得：

$$

\begin{align}f(x) = \frac{1}{(\sqrt{2π})^{d}\left( \prod\lambda_i \right)^\frac{1}{2}}e^{-\frac{ 1}{2} (x\  -\  \mu)^\mathrm{T}\ \mathbf{V}  {\mathbf {\Lambda}}^{-1}  \mathbf{V^T}\  (x\  -\  \mu)}  \tag 9\end{align}

$$

然后，根据公式$(8)$，很容易计算其协方差矩阵的逆矩阵，即：

$$

\mathbf{\Sigma}^{-1} =  \mathbf{V} \mathbf {\Lambda}^{-1} \mathbf{V^T}  \tag {10}

$$

而且，由于[方阵的行列式等于特征值之积](https://eipi10.cn/linear-algebra/2019/12/07/eigenvalue_and_eigenvector/#%E6%96%B9%E9%98%B5%E7%9A%84%E8%BF%B9%E5%92%8C%E8%A1%8C%E5%88%97%E5%BC%8F)，也就是：

$$

\left|\Sigma\right| =  \prod\lambda_i  \tag {11}

$$

最后把公式$(10)$和$(11)$带入公式$(9)$，可得：

$$

\begin{align}
f(x) &=  \frac{1}{(\sqrt{2π})^{d}\left|\Sigma\right|^\frac{1}{2}}e^{-\frac{ 1}{2} (x\  -\  \mu)^\mathrm{T}\  \Sigma^{-1}\  (x\  -\  \mu)}
\end{align}

$$

证毕。显见，当只有一个变量时，公式会退化到简单的一元正态分布的公式。

### 正态分布的几何意义

![image-20210508183437512](/assets/images/image-20210508183437512.png)

下面来梳理上面的证明过程，以二元正态分布为例。

- 独立标准二元分布

  如上面左图所示，两个随机变量相互独立，方差都是1。

- 独立二元正态分布

  如上面中图所示，两个随机变量相互独立，但方差在X轴是4，在Y轴是0.5。从图形上看，对左图在X轴方向的拉伸一倍，在Y轴缩减一倍，可以得到中图。

- 非独立二元正态分布

  如上面右图所示，两个随机变量不相互独立。从图形上看，中图逆时针旋转30度得到右图。

从独立标准二元正态分布到非独立二元正态分布，经历了伸缩和旋转的的线性变换过程，相关代码如下：

~~~python
import numpy as np
import math
import matplotlib.pyplot as plt
import random
from sklearn.decomposition import PCA 

def normal(center, radius, num=100, seed=2009):
    np.random.seed(seed)
    angles = np.linspace(0, 2*math.pi, num=num)
    x0, y0 = center
    x = np.random.normal(x0, 1, num)
    y = np.random.normal(y0, 1, num)    
    return np.array([x, y])

def transfer(m, data, center=True):
    if center==True:     
        center = np.mean(data, axis=1, keepdims=True)
        transfer_data = m.dot((data - center)) + center
    else:
        transfer_data = m.dot(data)
    return transfer_data, m    

def rotate(theta, data, center=True):
    m = np.array([[math.cos(theta), -math.sin(theta)],
                  [math.sin(theta), math.cos(theta)]])
    return transfer(m, data, center)

def scale(s, data, center=True):
    m = np.diag(s)
    return transfer(m, data, center)

def get_data(num, scale_rate=[2, 0.5], rotate_angle=30, seed=2009):
    # 1. 生成样本。每个样本坐标来自独立分布的正态分布
    data = normal([1, 1], 1, num=num, seed=seed) 
    print('data.shape =', data.shape)

    # 2. 伸缩 
    scale_data, scale_m = scale(scale_rate, data, center=True)

    # 3. 旋转
    theta = 30/180*math.pi
    rotate_data, rotate_m  = rotate(rotate_angle/180*math.pi, scale_data, center=True)   
    
    return data, scale_data, rotate_data

def eig(data):
    d, n = data.shape
          
    cov = np.cov(rotate_data)
    # 也可以使用下面两行来计算协方差矩阵
    # centered_data = data - np.mean(data, axis=1, keepdims=True)
    # cov = 1/(n-1)*(centered_data) @ centered_data.T
    
    eigenvalue, eigenvector = np.linalg.eig(cov)    
    return eigenvalue, eigenvector
    
def plot_scatter(data, color):
    plt.scatter(data[0, :], data[1, :], color=color, alpha=0.5, s=1) 
    
    print('-'*50)
    
    # 计算协方差矩阵的特征向量
    eigenvalue, eigenvector = eig(data)
    
    print('eigenvalue = {}'.format(eigenvalue))
    print('eigenvector = \n{}'.format(eigenvector))
    center = np.mean(data, axis=1)
    B = eigenvector 

    plt.quiver([center[0],center[0]], [center[1],center[1]], B[0,:], B[1,:], angles='xy', scale_units='xy',  scale=1)
    plt.text(*B[:,0]+center, '$v_1$', size=12, color='black')
    plt.text(*B[:,1]+center, '$v_2$', size=12, color='black')
    
    plt.xlim([center[0]-4, center[0]+4])
    plt.ylim([center[1]-4, center[1]+4])
    plt.grid(linestyle='-.')    
    
data, scale_data, rotate_data = get_data(1000)

# 图形展示
plt.figure(figsize=(18, 5.5))

plt.subplot(131)
plot_scatter(data, color='red')

plt.subplot(132)
plot_scatter(scale_data, color='green')

ax3 = plt.subplot(133)
plot_scatter(rotate_data, color='blue')

plt.show()
~~~

![image-20210518160753189](/assets/images/image-20210518160753189.png)

上一节的证明过程，刚好是上面线性变换的反向操作，从图形上看，就是先把右图旋转为中图，然后再伸缩到左图。再来看分布密度函数公式$(9)$，还可以进行如下推导。

$$

\begin{align}
f(x) &= \frac{1}{(\sqrt{2π})^{d}\left( \prod\lambda_i \right)^\frac{1}{2}}e^{-\frac{ 1}{2} (x\  -\  \mu)^\mathrm{T}\ \mathbf{V}  {\mathbf {\Lambda}}^{-1}  \mathbf{V^T}\  (x\  -\  \mu)}  \\
f(x) &= \frac{1}{(\sqrt{2π})^{d}  }  e^{-\frac{ 1}{2} \left( {\mathbf {\Lambda}}^{-\frac 1 2} \mathbf{V^T}(x\  -\  \mu) \right)^\mathrm{T}\   {\mathbf {\Lambda}}^{-\frac 1 2} \mathbf{V^T}\  (x\  -\  \mu)}   \frac 1 {\sqrt \lambda_1} \frac 1 {\sqrt \lambda_2} \cdots \frac 1 {\sqrt \lambda_d}  
\end{align}

$$

其中$${\mathbf {\Lambda}}^{-\frac 1 2}  = diag(\mathbf {\frac 1 {\sqrt \lambda_1}},\mathbf {\frac 1 {\sqrt \lambda_2}}, \cdots,  \mathbf {\frac 1 {\sqrt \lambda_d}})$$，然后在两边求积分，可得：

$$

\begin{align}
\int \cdots \int f(x)  \mathbf d x_1 \mathbf d x_2  \cdots \mathbf d x_d &= \int \cdots \int \frac{1}{(\sqrt{2π})^{d}  }  e^{-\frac{ 1}{2} \left( {\mathbf {\Lambda}}^{-\frac 1 2} \mathbf{V^T}(x\  -\  \mu) \right)^\mathrm{T}\   {\mathbf {\Lambda}}^{-\frac 1 2} \mathbf{V^T}\  (x\  -\  \mu)}  \mathbf d \frac {x_1 - \mu_1} {\sqrt \lambda_1}  \mathbf d \frac {x_2- \mu_2}  {\sqrt \lambda_2} \cdots \mathbf d  \frac {x_d- \mu_d}  {\sqrt \lambda_d}  \\

\int \cdots \int f(x)  \mathbf d x_1 \mathbf d x_2  \cdots \mathbf d x_d &= \int \cdots \int \frac{1}{(\sqrt{2π})^{d}  }  e^{-\frac{ 1}{2} \left(  \mathbf{V^T} \frac {x\  -\  \mu} {\mathbf {\sqrt \lambda}} \right)^\mathrm{T}\    \mathbf{V^T} \frac {x\  -\  \mu} {\mathbf {\sqrt \lambda}}}  \mathbf d \frac {x_1 - \mu_1} {\sqrt \lambda_1}  \mathbf d \frac {x_2- \mu_2}  {\sqrt \lambda_2} \cdots \mathbf d  \frac {x_d- \mu_d}  {\sqrt \lambda_d}
\end{align}

$$

其中${\sqrt \lambda} = \left[ \begin{matrix} \mathbf {\frac 1 {\sqrt \lambda_1}} &\mathbf {\frac 1 {\sqrt \lambda_2}} &  \cdots & \mathbf {\frac 1 {\sqrt \lambda_d}} \end{matrix}\right]^\mathrm{T}$，于是显见。

- $\mathbf{V^T} \frac {x\  -\  \mu} {\mathbf {\sqrt \lambda}} $表示对坐标进行缩放，然后进行线性变换，相当于把上面图片中，右图的椭圆变成了左图的圆了。
- $\left( \prod\lambda_i \right)^\frac{1}{2}$表示微分变换时的系数之积。通俗的理解，既然前方进行了伸缩，要保持平衡的话，就要把缩放的比例反向除回去。

## 马氏距离

马氏距离（Mahalanobis distance）是由印度统计学家马哈拉诺比斯(P. C. Mahalanobis)提出的，是欧氏距离的一种推广。它通过协方差来计算两点之间距离，是一种有效的计算两个未知样本集的相似度的方法。与欧氏距离不同的是它考虑到各种特性之间的相关性。它的定义如下：

对于一个均值为$$\mu =(\mu _{1},\mu _{2},\mu _{3},\dots ,\mu _{d})^{T}$$，协方差矩阵为Σ的多变量向量$$x=(x_{1},x_{2},x_{3},\dots ,x_{d})^{T}$$，其马氏距离为：

$$

D_{M}(x)={\sqrt {(x-\mu )^{T}\Sigma ^{-1}(x-\mu )}}

$$

从形式上看，马氏距离和正态分布公式的其中一部分完全相同。于是，正如上节分析所示，可以把马氏纪录理解为，把样本点缩放（即$\frac {x\  -\  \mu} {\mathbf {\sqrt \lambda}} $），然后进行线性变换到特征矩阵所在空间（即$$\mathbf{V^T} \frac {x\  -\  \mu} {\mathbf {\sqrt \lambda}} $$），最后求再这个空间的欧氏距离，也就说是马氏距离考虑了样本相关性的欧式距离。

对于下面图中的数据，分别计算点1和点2到中心的距离，它们的欧式距离是相等的。但很明显，根据正态分布公式，点1出现的概率比点2要小，即认为点1距离中心点的距离要更远，马氏距离考虑到了这一点，所以它比欧式距离更合理。

![img](/assets/images/091418399468508.gif)

同理，马氏距离也可以定义为两个服从同一分布并且其协方差矩阵为$\Sigma$的随机变量${\vec {x}}$ 与${\vec {y}}$的差异程度：

$$

d({\vec {x}},{\vec {y}})={\sqrt {({\vec {x}}-{\vec {y}})^{T}\Sigma ^{-1}({\vec {x}}-{\vec {y}})}}

$$

## 主成分分析

![image-20210512145234002](/assets/images/image-20210512145234002.png)

主成分分析（Principal Component Analysis），简称PCA，是最重要的降维算法之一。PCA的思想是对数据进行线性变换，然后在新的坐标系中，选取那些占据了绝大部分方差的维度，这些维度就称为主成分。PCA常用于用于数据压缩，噪音消除，运用及其广泛。

PCA所使用的线性变换就是协方差矩阵的特征向量矩阵，特征向量矩阵是一个正交变换，正交变换的几何意义是旋转，对数据之间的关系没有改变。

### 证明

下面来证明PCA的数学原理，即特征向量矩阵是方差最大化的线性变换。为了简化，先对协方差矩阵做一些简化。

设$\mathbf X = \begin{bmatrix} x_1-\mu & x_2-\mu & \cdots & x_n-\mu \end{bmatrix}$ ，即中心化的矩阵，协方差矩阵可以简化为：

$$

\Sigma = \frac 1 {n-1} \mathbf X \cdot \mathbf X^{\mathbf T}

$$

其中$\mathbf X$是$$d\times n$$矩阵，$d$表示随机变量个数，$n$表示样本个数。

设$\mathbf U = \begin{bmatrix} u_1 & u_2 & \cdots & u_d \end{bmatrix} $是要求解的正交矩阵，其中$u_1$是方差最大的维度，$u_2$是第二大的，以此类推。

再设$u$是$\mathbf U$其中任意一个维度向量，则$u^{\mathbf T} \mathbf X$ 表示在样本点在维度$u$中的投影（坐标），于是在这个维度上的方差可以表示如下：

$$

\begin{align}
\sigma &= \frac 1 {n-1} u^{\mathbf T} \mathbf X(u^{\mathbf T} \mathbf X)^{\mathbf T}  \\
 &= \frac 1 {n-1} u^{\mathbf T} \mathbf X\mathbf X^{\mathbf T} u  \\
 &=  u^{\mathbf T}  \left(\frac 1 {n-1} \mathbf  X \mathbf X^{\mathbf T} \right) u  \\
 &=  u^{\mathbf T}  \Sigma  u  \\
\end{align}

$$

然后带入$\mathbf{\Sigma} =  \mathbf{V} \mathbf {\Lambda} \mathbf{V^T} $，可得：

$$

\begin{align}
\sigma &=  u^{\mathbf T} \mathbf{V} \mathbf {\Lambda} \mathbf{V^T} u  \\
\end{align}

$$

由于协方差矩阵是对称矩阵，其特征值非负，设$\lambda_1\geq \lambda_2 \geq \cdots \geq \lambda_d \geq 0$，$z = \mathbf{V^T} u$，带入上式可得：  

$$

\begin{align} 
\sigma &=  z^{\mathbf T}  \mathbf {\Lambda}z  \\
	   &=  z_1^2\lambda_1 + z_2^2\lambda_2 + \cdots +  z_d^2\lambda_d \tag {12} \\  
	   & \leq z_1^2\lambda_1 + z_2^2\lambda_1 + \cdots +  z_d^2\lambda_1 \\
	   & \leq (z_1^2 + z_2^2 + \cdots +  z_d^2)\lambda_1
\end{align}

$$

由于$z^{\mathbf T}z=1$，即$z_1^2 + z_2^2 + \cdots +  z_d^2=1 $，可以推得：

$$

\begin{align}
\sigma & \leq   \lambda_1

\end{align}

$$

不难看出，当且仅当$z_1=1, \ z_2=z_3= \cdots =z_d=0 $，上面不等式等号成立，于是可以推出：

$$

\begin{align}
z &= \mathbf{V^T} u \\
\begin{bmatrix} 1 \\ 0  \\ \vdots \\ 0 \end{bmatrix} &=\mathbf{V^T} u \\
 u &= \mathbf{v_1}
\end{align}

$$

由此，证明了方差最大的维度，刚好就是最大特征值所对应的特征向量，也就是说$u_1=v_1$。下面，继续来证明$u_2=v_2$。

$$

\begin{align}
z_1 &= v_1^{\mathbf T} u \\
z_1 &= u_1^{\mathbf T} u \\
\end{align}

$$

$$

z_1 = \begin{equation}  
\left\{  
\begin{array}{lcl}  
 1        &  & if\ u=u_1\\  
 0 &  & if\ u \neq u_1 
\end{array}  
\right.
\end{equation}

$$

把上面结果带入公式$(12)$，当$\ u \neq u_1$，推得：

$$

\begin{align}
\sigma &=  z_1^2\lambda_1 + z_2^2\lambda_2 + \cdots +  z_n^2\lambda_d  \\  
	   &=   0 + z_2^2\lambda_2 + z_3^2\lambda_3+ \cdots +  z_n^2\lambda_d  \\
	   & \leq  z_2^2\lambda_2 + \cdots +  z_n^2\lambda_2 \\
	   & \leq (0 + z_2^2 + \cdots +  z_n^2)\lambda_2  \\
	   & \leq (z_1^2 + z_2^2 + \cdots +  z_n^2)\lambda_2  \\
	   & \leq \lambda_2
\end{align}

$$

要满足等式成立，条件是$z_1=0, \ z_2=1， z_3= z_4= \cdots =z_d=0$，可以推得：

$$

\begin{align}
z &= \mathbf{V^T} u \\
\begin{bmatrix} 0 \\ 1  \\ 0 \\ \vdots \\ 0 \end{bmatrix} &=\mathbf{V^T} u \\
 u &= \mathbf{v_2}
\end{align}

$$

由此得证$$u_2=v_2$$。

同理可以证明其它维度依次等于对应的特征向量，即$\mathbf U = \mathbf V $，证毕。

### 应用

我们可以使用`sklearn.decomposition.PCA`直接来进行PCA的操作，下面是一个例子。

~~~python
def show_pca(pca):
    print('特征(随机变量)个数：', pca.n_features_) 
    print('样本数：', pca.n_samples_) 
    print('主成分(特征向量)：\n{}'.format(np.round(pca.components_, 3)))
    print('方差(特征值)：', np.round(pca.explained_variance_, 3))
    print('方差比例：', pca.explained_variance_ratio_)  
    print('噪音方差：', pca.noise_variance_) 
    print('噪音方差：', pca.singular_values_)    
    
_, _, data = get_data(8)
center = np.mean(data, axis=1, keepdims=True)
print('data =\n{}'.format(np.round(data, 3)))

# PCA： 不降维，只是把当前数据变换到特征矩阵所在空间。
pca=PCA(n_components=2)   
pca_data=pca.fit_transform(data.T).T
print('-'*50)
print('pca_data =\n{}'.format(np.round(pca_data, 3)))
# 还原到原始数据
restore_data = pca.components_.T @ pca_data + center
np.testing.assert_array_almost_equal(data, restore_data)
print('restore_data =\n{}'.format(np.round(restore_data, 3)))

print('-'*50)
show_pca(pca)
~~~

![image-20210519140442142](/assets/images/image-20210519140442142.png)

> 在机器学习中，矩阵的第一个维度都是样本个数，所以`sklearn.decomposition.PCA`要求传入一个$n\times d$的矩阵，也就是说每一行是一个样本，而在线性代数中，为了更加体现数学的意义，一般把一个样本当成向量，所以`numpy.cov`中要求的矩阵是$d\times n$。

我们也可以手工来计算。

~~~python
eigenvalue, eigenvector = eig(data)
print('eigenvalue = {} {}'.format(np.round(eigenvalue, 3), eigenvalue.shape))
print('eigenvector = \n{} {}'.format(np.round(eigenvector, 3), eigenvector.shape))

pca_data = eigenvector.T @ (data - center)
print('pca_data =\n{}'.format(np.round(pca_data, 3)))
~~~

![image-20210519140554930](/assets/images/image-20210519140554930.png)

可以发现，手工求出的特征矩阵，每一列是一个特征向量，而`sklearn.decomposition.PCA`得到的特征矩阵，每一行是一个特征向量。另外，需要注意，它们的特征向量，方向刚好相反。

上面的例子没有降维，看看实际降维的代码。

~~~python
# PCA： 降维
pca=PCA(n_components=1)
pca_data=pca.fit_transform(data.T).T
print('-'*50)
print('pca_data =\n{}'.format(np.round(pca_data, 3)))

# 手工进行PCA
print('-'*50)
eigenvalue, eigenvector = eig(data)

center = np.mean(data, axis=1, keepdims=True)
pca_data = eigenvector[:, 0].T @ (data - center)
print('pca_data =\n{}'.format(np.round(pca_data, 3)))
~~~

![image-20210519142501277](/assets/images/image-20210519142501277.png)

## 总结

通过协方差矩阵在正态分布，马氏距离和主成分分析中的应用，我们可以看到方差代表距离的叠加，距离可以转化为概率，协方差矩阵本质上代表了一个线性变换，即特征向量矩阵，这就是它的意义。

## 参考

- [协方差矩阵](https://baike.baidu.com/item/%E5%8D%8F%E6%96%B9%E5%B7%AE%E7%9F%A9%E9%98%B5)
- [多元高斯分布（The Multivariate normal distribution）](https://www.cnblogs.com/bingjianing/p/9117330.html)
- [马哈拉诺比斯距离](https://zh.wikipedia.org/wiki/%E9%A9%AC%E5%93%88%E6%8B%89%E8%AF%BA%E6%AF%94%E6%96%AF%E8%B7%9D%E7%A6%BB)
- [关于Mahalanobis距离的笔记](https://www.cnblogs.com/chaosimple/p/4153178.html)
- [机器学习之距离与相似度计算](https://www.biaodianfu.com/distance.html)
- [主成分分析（PCA）原理总结](https://www.cnblogs.com/pinard/p/6239403.html)
