
- 线性回归的最大似然推导
- 线性回归equation的两种推导方法
- 线性回归的梯度下降公式。
- 非线性最小二乘

线代随笔11-线性回归相关的向量求导 http://bourneli.github.io/linear-algebra/calculus/2016/04/28/linear-algebra-11-derivate-of-linear-regression.html  
线代随笔12-线性回归的矩阵推导 http://bourneli.github.io/linear-algebra/calculus/2016/04/30/linear-algebra-12-linear-regression-matrix-calulation.html   
线性模型（二）-- 线性回归公式推导 http://blog.csdn.net/fleurdalis/article/details/54931721  
矩阵导数  https://ccjou.wordpress.com/2013/05/31/%E7%9F%A9%E9%99%A3%E5%B0%8E%E6%95%B8/

### 模型
$ \hat y = Xw$

$Xw$, 其实可以理解为X的各个向量和w的内积。而内积的意义： 

$a \cdot b =  a \cdot \frac {b} {|b|} * |b| $  表示a向量在 $ \frac {b} {|b|} $上的投影再乘以$|b|$。

这样看来这个模型可以理解为把X投影到w的向量空间上。和cs231n里面的描述有相似之处。

**Interpretation of linear classifiers as template matching**
Another interpretation for the weights w is that each row of w corresponds to a template (or sometimes also called a prototype) for one of the classes. The score of each class for an image is then obtained by comparing each template with the image using an inner product (or dot product) one by one to find the one that “fits” best. With this terminology, the linear classifier is doing template matching, where the templates are learned. 

Another way to think of it is that we are still effectively doing Nearest Neighbor, but instead of having thousands of training images we are only using a single image per class (although we will learn it, and it does not necessarily have to be one of the images in the training set), and we use the (negative) inner product as the distance instead of the L1 or L2 distance.

线性分类器可以看成一种template matching（把X投影到w的向量空间上），和kNN不同的地方在于，不需要计算两两之间的距离，而只需要计算每个样本和w的距离（内积，也就是投影）。


### Cost函数

$\begin{align}
J(w) &= \sum_{i=1}^m (y_i-\hat y_i)^2    \\
     &= \sum_{i=1}^m (y_i-x_i w)^2    \\
     &= \frac 1 {2m} (Xw - y)^\mathrm{T}(Xw - y)     
\end{align}$

### Equation

$w =  {(X^\mathrm{T}X)^{-1}}Xy $ 

上面的公式可以这样来推导而出。

线性回归可以理解为求解w满足下面方程式的最优解（最优解的定义是）

$X  w = y$ 

$w =  {(X^\mathrm{T}X)^{-1}}Xy $

### 梯度

$\nabla{w} = \frac 1 m X^\mathrm{T}(Xw - y)  $ 

$ w|_{\nabla{w} = 0}  = (X^\mathrm{T}X )^{-1}X^\mathrm{T}y$

# 参见

- [CS231n Linear Classification notes](http://cs231n.github.io/linear-classify/)
- [机器学习实战教程：线性回归基础篇之预测鲍鱼年龄](http://cuijiahua.com/blog/2017/11/ml_11_regression_1.html) 这里面介绍了线性回归，加权线性回归，局部加权线性回归。
