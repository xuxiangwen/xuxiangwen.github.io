## MNIST

[MNIST](http://yann.lecun.com/exdb/mnist/)（Mixed National Institute of Standards and Technology）数据集是著名的手写数字数据集，被誉为数据科学领域的`果蝇`。

![img](images/8389494-c279133be28eb263.webp)

数据分为四部分。

| 数据文件                                                     | 描述         | 数据量 |
| ------------------------------------------------------------ | ------------ | ------ |
| [train-images-idx3-ubyte.gz](http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz) | training图片 | 60,000 |
| [train-labels-idx1-ubyte.gz](http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz) | training标签 | 60,000 |
| [t10k-images-idx3-ubyte.gz](http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz) | training图片 | 10,000 |
| [t10k-labels-idx1-ubyte.gz](http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz) | training标签 | 10,000 |

其中每张图片由$28 \times 28$ 个像素点构成，每个像素点用一个灰度值($0-255$)表示。

### 数据文件下载

~~~python
import os
from qbz95.ml3.utils.data.datasets import MNIST

local_path = os.path.join('.', 'data/mnist')
train_data_path, train_label_path, test_data_path, test_label_path = MNIST.download(local_path)
~~~

