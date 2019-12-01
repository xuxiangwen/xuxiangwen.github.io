



## Basic

### Tensor

Tensor和 NumPy   ndarray非常相似，不同的是，Tensor可以使用GPU来加速计算。

| 操作                               | numpy                     | torch                              |
| ---------------------------------- | :------------------------ | ---------------------------------- |
| empty                              | np.empty([5, 3])          | np.empty(5, 3)                     |
| rand 均匀分布                      | np.random.rand(5, 3)      | torch.rand(5, 3)                   |
| randn 正态分布                     | np.random.randn(5, 3)     | torch.randn(5, 3)                  |
| zeros                              | np.zeros([5, 3])          | torch.zeros(5, 3)                  |
| ones                               | np.ones([5, 3])           | torch.ones(5, 3)                   |
| construct from data                | np.array([5.5, 3])        | torch.Tensor([5.5, 3])             |
| contruct: 使用原对象的shape和dtype | np.random.randn(*x.shape) | torch.randn_like(x)                |
| shape                              | x.shape                   | x.size() or x.shape                |
| 加法/减法                          | x + y，x - y              | x + y，x - y                       |
| 点乘                               | x * y                     | x * y                              |
| 乘法（叉乘）                       | x.dot(y) or x @ y         | x.mm(y)  or x @ y                  |
| adds x to y                        |                           | y.add_(x)                          |
| 获取部分数据                       | x[:, 1]                   | x[:, 1]                            |
| reshape                            | x.reshape((-1, 3))        | x.view(-1, 4)  or x.reshape(-1, 3) |
| 转置                               | x.T                       | x.t() or x.T                       |
| 向量长度（范数）                   | np.linalg.norm(x)         | x.norm()                           |
|                                    |                           |                                    |
|                                    |                           |                                    |
|                                    |                           |                                    |
|                                    |                           |                                    |
|                                    |                           |                                    |

#### numpy to torch

~~~
x = np.random.rand(5, 3)
torch.from_numpy(x)
~~~

#### torch to numpy

~~~
x = torch.randn(5, 3)
x.numpy()
~~~

### CUDA Tensor

~~~
if torch.cuda.is_available():
    device = torch.device("cuda")          # a CUDA device object
    x = torch.rand(5, 3)
    y = torch.ones_like(x, device=device)  # directly create a tensor on GPU
    x = x.to(device)                       # or just use strings ``.to("cuda")``
    z = x + y
    print(z)
    print(z.to("cpu", torch.double))       # ``.to`` can also change dtype together
~~~

