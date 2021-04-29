### 增加维度（dimension）的几种方法

有三种方法，以`np.expand_dims`最佳。

~~~python
import numpy as np
a = np.array([[2, 1, 3], [1, 2, 4]])
print(a, a.shape)

print('-'*50)
a1 = a.reshape(a.shape + (1,))
print(a1, a1.shape)

print('-'*50)
a1 = a[..., np.newaxis]
print(a1, a1.shape)

print('-'*50)
a1 = np.expand_dims(a, axis=-1)
print(a1, a1.shape)
~~~

![image-20210317193555767](images/image-20210317193555767.png)

### 多分类

- **OvR（One vs Rest）**，一对剩余的意思，有时候也称它为 OvA（One vs All）

  n 种类型的样本进行分类时，**分别**取一种样本作为一类，将剩余的所有类型的样本看做另一类，这样就形成了 **n 个**二分类问题，使用逻辑回归算法对 n 个数据集训练出 n 个模型，将待预测的样本传入这 n 个模型中，所得概率最高的那个模型对应的样本类型即认为是该预测样本的类型。

  ![img](images/1355387-20180729220050227-2123786111.png)

- **OvO（One vs One）**

  n 类样本中，每次挑出 2 种类型，两两结合，一共有 $C_n^2$种二分类情况，使用$C_n^2$ 种模型预测样本类型，有 $C_n^2$个预测结果，种类最多的那种样本类型，就认为是该样本最终的预测类型

  ![img](images/1355387-20180730081828969-80068959.png)