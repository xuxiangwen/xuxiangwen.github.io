核主成分分析（Kernel Principal Component Analysis）简称KPCA，它是对[主成分分析（PCA）](https://eipi10.cn/mathematics/2021/05/12/covariance_matrix/#%E4%B8%BB%E6%88%90%E5%88%86%E5%88%86%E6%9E%90)的扩展，PCA通过把线性变换把数据旋转到特征矩阵所在向量空间，消除了随机变量之间的线性相关，然而这些操作对于高阶的相关性就无能为力，而KPCA可以部分解决这个问题。KPCA假设，样本数据是高维到低维的投影，这种投影会带来信息的丢失，正如：一棵大树在正午的投影是一个椭圆，我们很难区分哪里是树干，哪里是树冠，也就是说，在低维空间无法区分很多信息，基于此，KPCA通过映射函数把数据映射到高维空间，然后再进行PCA操作，这样的操作可以更大程度的对变量的相关性进行消除，从而获取更有意义的主成分。本文将对KPCA进行通俗易懂的详细推导，并实际比较KPCA和PCA，帮助大家更加深刻的理解它们。

## 从低维到高维

KPCA通过映射函数把数据映射到高维空间，这带来两个问题：

- 映射函数如何选取呢？
- 高维空间要多少维才合适呢？

对于第一个问题没有确定答案，因为数学上的相关函数太多了。那我们先看看第二个问题，由于我们只看到低维的样本数据，很难想象高维数据的特征，换句话说，高维数据有无限的可能，正如上面的例子，一个二维椭圆投影，在三维空间，可以是一棵树，也可以是一个球，而在四维空间，可能性就更多了。由此，如果映射后的高维空间维数越多，或许更加能够反应这种多样的可能性，也就是说，我们希望高维空间的维度高一些。

然而，选用维度很高的映射，又带来计算的问题。下面是常规的计算步骤：

1. 函数映射。

   设

   - $\mathbf X=[\begin{matrix} x_1 & x_2 & \dots & x_n]\end{matrix}$是一个$d\times n $矩阵，代表有$n$个样本，每个样本维度是$d$ 。
   - 映射函数为$\Phi$，映射后的矩阵是$\Phi(\mathbf X) $，它是$$D \times n $$矩阵，$D（D\gg d）$。
   - 一个样本的转换时间是$t_\Phi $。

   则所有样本的转换时间是$n \times t_\Phi$。

2. 计算协方差矩阵。

   设中心化的数据记为$\tilde\Phi(\mathbf X)$，即
   $$
   \tilde\Phi(  \mathbf X)=\Phi(\mathbf X)-\bar\Phi  
   $$
   其中$\bar\Phi$表示均值，是一个$D$维向量。由此，协方差矩阵$\mathbf C$表示为：
   $$
   \mathbf C = \frac{1}{n-1}\tilde\Phi(\mathbf X)\tilde\Phi(\mathbf X)^T     
   $$
   
   要计算这个协方差矩阵，需要执行$D^2n^2$次乘法，$D^2(n-1)$次加法。
   
3. 特征值分解。

   特征值分解是一个矩阵对角化的过程，其时间复杂度是$D^3$。

4. 选取top k个特征值，及其特征向量，计算新的样本。

   需要执行$kD^2n$次乘法，$D^2(n-1) $次加法。

从上面的步骤可以看出，$D$对性能的影响很大，当$D$变的很大时，计算的空间和时间复杂度急剧上升，这无疑和我们希望$D$尽可能大一些构成矛盾。有何破解之法吗？

## 核方法和核技巧

破解之法就是核方法和核技巧。在具体展开之前，让我们来看一个推导特征值分解的性质。

根据特征值分解的定义，可知：
$$
\begin{align}
\mathbf{C} &=  \mathbf{V} \mathbf {\Lambda} \mathbf{V^T} \\
\mathbf{C} \mathbf{V} &=  \mathbf{V} \mathbf {\Lambda}  \\
\frac{1}{n-1}\tilde\Phi(\mathbf X)\tilde\Phi(\mathbf X)^{\mathbf T} \mathbf{V} &=  \mathbf{V} \mathbf {\Lambda} 
\end{align}
$$
然后，使用$\tilde\Phi(\mathbf X)^T$乘以等式两边，可得：
$$
\begin{align}
\frac{1}{n-1}\tilde\Phi(\mathbf X)^{\mathbf T}\tilde\Phi(\mathbf X)\tilde\Phi(\mathbf X)^{\mathbf T} \mathbf{V} &=  \tilde\Phi(\mathbf X)^{\mathbf T}\mathbf{V} \mathbf {\Lambda}  
\end{align}
$$
设$\mathbf C^{'} = \tilde\Phi(\mathbf X)^{\mathbf T}\tilde\Phi(\mathbf X)$， $\mathbf U = \tilde\Phi(\mathbf X)^{\mathbf T} \mathbf{V}$，$\mathbf {\Lambda^{'} }= (n-1) \mathbf  \Lambda $，上面公式可以变成。
$$
\begin{align}
\mathbf C^{'} \mathbf{U} &=  \mathbf U \mathbf {\Lambda^{'} }   \tag 3
\end{align}
$$
可以发现，上面的式子和[特征值分解](https://eipi10.cn/linear-algebra/2019/12/07/eigenvalue_and_eigenvector/)的公式完全一致。下面来验证一下$\mathbf U$是不是正交矩阵，设$u_i, u_j$为其中任意两个向量。
$$
\begin{align}
u_i^{\mathbf T}u_j &=  \left(\tilde\Phi(\mathbf X)^{\mathbf T} v_i \right)^{\mathbf T}\tilde\Phi(\mathbf X)^{\mathbf T} v_j \\
&=  v_i^{\mathbf T}\tilde\Phi(\mathbf X)\tilde\Phi(\mathbf X)^{\mathbf T} v_j \\
&= v_i^{\mathbf T} (n-1)\mathbf C v_j \\
&= (n-1) v_i^{\mathbf T} \mathbf{V} \mathbf {\Lambda} \mathbf{V^T}   v_j \\
&=  v_i^{\mathbf T} \mathbf{V} (n-1) \mathbf {\Lambda} \mathbf{V^T}   v_j \\
&= v_i^{\mathbf T} \mathbf{V} \mathbf {\Lambda^{'}} \mathbf{V^T}   v_j \\
\end{align}
$$
设$ \mathbf {\Lambda^{'}} = diag(\lambda_1^{'}, \lambda_2^{'}, \cdots, \lambda_D^{'})$，不难得出如下公式：
$$
u_i^{\mathbf T}u_j  = \begin{equation}  
\left\{  
\begin{array}{lcl}  
 \lambda_i^{'}        &  & if\ i=j\\  
 0 &  & if\  i \neq j
\end{array}  
\right.
\end{equation}
$$
接下来还需要把$\mathbf U$变成一个单位向量，也就是设$\mathbf V^{'}  = \frac {\mathbf U } {\mathbf {\sqrt {\Lambda^{'} }}} $，即$\mathbf V^{'} = \frac {\tilde\Phi(\mathbf X)^{\mathbf T} \mathbf{V}} {\mathbf {\sqrt {\Lambda^{'} }}} $，公式$(3)$可以推得。
$$
\begin{align}
\mathbf C^{'} \mathbf{V}^{'} &=  \mathbf V^{'} \mathbf {\Lambda^{'} }  
\end{align}
$$
其中

- $\mathbf C^{'} = \tilde\Phi(\mathbf X)^{\mathbf T}\tilde\Phi(\mathbf X)$，是一个$n \times n$矩阵。
- $\mathbf V^{'} = \frac {\tilde\Phi(\mathbf X)^{\mathbf T} \mathbf{V}} {\mathbf {\sqrt {\Lambda^{'} }}} $，是一个$n\times D$正交矩阵。
- $\mathbf {\Lambda^{'} }= (n-1) \mathbf  \Lambda $，是一个$D\times D$对角矩阵。



**核方法** 是一类把低维空间的非线性可分问题，转化为高维空间的线性可分问题的方法。。核方法的理论基础是



## 

核技巧（Kernal Trick）是一种利用核函数直接计算 ![[公式]](https://www.zhihu.com/equation?tex=%5Clangle+%5Cphi%28x%29%2C%5Cphi%28z%29+%5Crangle%E2%80%8B) ，从而加速核方法计算的技巧。





## 实际应用

是重要的降维方法之一，PCA的本质是选取特征值最大的几个对应特征向量，对数据进行降维，然而这样也带来几个问题：

- PCA容易收到离群点的影响。如果有若干离群点，将会对特征矩阵有极大的影响
- PCA隐含假定数据是正态分布，如果数据不是正态分布，作用大打折扣。
- 特征矩阵本质上对数据进行旋转，所以PCA只能处理数据的线性关系。
- PCA忽略的特征值，可能也包含很多有用信息。



### 离群点的例子

非正态分布。

## 参考

- [Kernel Principal Component Analysis](https://shengtao96.github.io/2017/06/09/Kernel-Principal-Component-Analysis/)

