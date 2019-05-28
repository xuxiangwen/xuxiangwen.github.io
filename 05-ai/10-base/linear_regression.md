### 模型
$ \hat y = Xw$

可以把$w$看作把$y$投影到$X$向量空间后的坐标.  所以$ \hat y  - y $得到的向量应该和$X$垂直. 也就是满足如下公式.

$
X^T (\hat y - y) = 0  
X^T (Xw - y) = 0  
w= {(X^\mathrm{T}X)^{-1}}Xy  
$







**Interpretation of linear classifiers as template matching**
Another interpretation for the weights w is that each row of w corresponds to a template (or sometimes also called a prototype) for one of the classes. The score of each class for an image is then obtained by comparing each template with the image using an inner product (or dot product) one by one to find the one that “fits” best. With this terminology, the linear classifier is doing template matching, where the templates are learned. 

Another way to think of it is that we are still effectively doing Nearest Neighbor, but instead of having thousands of training images we are only using a single image per class (although we will learn it, and it does not necessarily have to be one of the images in the training set), and we use the (negative) inner product as the distance instead of the L1 or L2 distance.

线性分类器可以看成一种template matching（把X投影到w的向量空间上），和kNN不同的地方在于，不需要计算两两之间的距离，而只需要计算每个样本和w的距离（内积，也就是投影）。


### Cost/损失函数

$\begin{align}
J(w) &= \frac 1 {2m}  \sum_{i=1}^m (y_i-\hat y_i)^2    \\
     &= \frac 1 {2m}  \sum_{i=1}^m (y_i-x_i w)^2    \\
     &= \frac 1 {2m} (Xw - y)^\mathrm{T}(Xw - y)     
\end{align}$

### Equation

$w =  {(X^\mathrm{T}X)^{-1}}Xy $ 

#### 方法一

上面的公式可以这样来推导而出。

线性回归可以理解为求解w满足下面方程式的最优解（最优解的定义是）

$X  w = y$ 

$w =  {(X^\mathrm{T}X)^{-1}}Xy $

### 梯度

$\nabla{w} = \frac 1 m X^\mathrm{T}(Xw - y)  $ 

$ w|_{\nabla{w} = 0}  = (X^\mathrm{T}X )^{-1}X^\mathrm{T}y$

# 参见

- [CS231n Linear Classification notes](http://cs231n.github.io/linear-classify/)
- [线代随笔05-向量投影](<http://bourneli.github.io/linear-algebra/2016/03/05/linear-algebra-05-projection-and-linear-regression.html>)
- [线代随笔11-线性回归相关的向量求导]( http://bourneli.github.io/linear-algebra/calculus/2016/04/28/linear-algebra-11-derivate-of-linear-regression.html)
- [线代随笔12-线性回归的矩阵推导](http://bourneli.github.io/linear-algebra/calculus/2016/04/30/linear-algebra-12-linear-regression-matrix-calulation.html )
- [机器学习实战教程：线性回归基础篇之预测鲍鱼年龄](http://cuijiahua.com/blog/2017/11/ml_11_regression_1.html) 这里面介绍了线性回归，加权线性回归，局部加权线性回归。





- 线性回归的最大似然推导
- 线性回归equation的两种推导方法
- 线性回归的梯度下降公式。
- 非线性最小二乘



2016 年 07月 07日 

[^LaTeX]: 支持 **LaTeX** 编辑显示支持，例如：$\sum_{i=1}^n a_i=0$， 访问 [MathJax][4] 参考更多使用方法。
[^code]: 代码高亮功能支持包括 Java, Python, JavaScript 在内的，**四十一**种主流编程语言。

[1]: https://www.zybuluo.com/mdeditor?url=https://www.zybuluo.com/static/editor/md-help.markdown
[2]: https://www.zybuluo.com/mdeditor?url=https://www.zybuluo.com/static/editor/md-help.markdown#cmd-markdown-高阶语法手册
[3]: http://weibo.com/ghosert
[4]: http://meta.math.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference