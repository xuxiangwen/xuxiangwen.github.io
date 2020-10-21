---
title: Conv2D
categories: deep-learning
date: 2020-10-20
---

本文将详细介绍Conv2d，并比较torch和tensorflow中的定义，然后通过它们实现经典的[LeNet](https://www.jiqizhixin.com/graph/technologies/6c9baf12-1a32-4c53-8217-8c9f69bd011b)。

## [torch.nn.Conv2d](https://pytorch.org/docs/stable/nn.html?highlight=conv2d#torch.nn.Conv2d)

~~~python
class torch.nn.Conv2d(
  in_channels,  # int，输入通道数
  out_channels, # int，输出通道数
  kernel_size,  # int或Tuple[int, int]，卷积核大小
  stride=1,     # int或Tuple[int, int]，滑动窗口，指每次卷积对原数据滑动stride个单元格
  padding=0,    # int或Tuple[int, int]，两边的空白填充（一般补0）
  dilation=1,   # int或Tuple[int, int]，膨胀系数，一个卷积核内部之间的间隔
  groups=1,     # int，Number of blocked connections from input channels to output channels. 
  bias=True,    # bool，是否启用bias
  padding_mode='zeros'  # str，选择有'zeros', 'reflect', 'replicate' or 'circular'
)
~~~

- input shape: $(N,C_{in}, H_{in},W_{in})$

  - $N$：batch size。也就是每次训练所使用的样本个数
  - $C_{in}$： 输入channel数量
  - $H_{in}$：输入图片的(像素)高度
  - $W_{in}$： 输入图性的(像素)宽度
  
- output shape: $(N,C_{out}, H_{out},W_{out})$

  - $N$：batch size。也就是每次训练所使用的样本个数
  - $C_{out}$： 输出channel数量
  - $H_{out}$：输出图片的(像素)高度
  - $W_{out}$：输出图片的(像素)宽度
  
  设$$\mathbf {S_{in}} = \begin{bmatrix} H_{in} & W_{in} \end{bmatrix}  $$，$$ \mathbf {S_{out} }= \begin{bmatrix} H_{out} & W_{out} \end{bmatrix}  $$，则
  $$
  \mathbf {S_{out}} = \lfloor \frac {\mathbf { S_{in}} + 2 \times \mathbf {padding}  - \mathbf {dilation} \circ (\mathbf {kernal\_size} -1 ) - 1} { \mathbf {stride}}  + 1 \rfloor
  $$
  上面的公式中，可以这样逐步理解。
  
  - $\mathbf {dilation} \circ (\mathbf {kernal\_size} -1 ) + 1 $： 表示一个卷积核所占的空间
  - ${\mathbf { S_{in}} + 2 \times \mathbf {padding}  - \mathbf {dilation} \circ (\mathbf {kernal\_size} -1 ) - 1}$：表示减去一个卷积核所占空间
  - $\frac {\mathbf { S_{in}} + 2 \times \mathbf {padding}  - \mathbf {dilation} \circ (\mathbf {kernal\_size} -1 ) - 1} { \mathbf {stride}}$ ：表示剩下空间可以容纳几个卷积核
  - $+ 1$：表示把第2步减去的卷积核，再加回来。
  - $\lfloor \cdots \rfloor$：表示向下取整。
  
  > 上面的逻辑同样适用于Conv1d，Conv3d
  
- dilation：膨胀系数，一个卷积核内部之间的间隔，默认为1，其卷积核如下图所示：

![image-20200113103126914](images/image-20200113103126914.png)

​		如果dilation=2，则如下图所示，dilation表示的是灰色格子之间的序号的间隔。

![image-20200113102809015](images/image-20200113102809015.png)

- 参数个数
    $$
    (H_{kernel\_size} \times W_{kernel\_size} \times C_{in} + 1) *C_{out}
    $$

    ~~~python
import torch 
    import torch.nn as nn
    
    conv2d = torch.nn.Conv2d(
        in_channels=3,
        out_channels=16,
        kernel_size=5
    )
    
    for parameters in conv2d.parameters():
        print(parameters.size())
    
    ## 上面两行代码等价于下面代码    
    print(conv2d.weights.size())
    print(conv2d.bias.size())
    ~~~
    
    ![image-20201020090817136](images/image-20201020090817136.png)

##  [tf.keras.layers.Conv2D](https://www.tensorflow.org/api_docs/python/tf/keras/layers/Conv2D)

~~~python
class tf.keras.layers.Conv2D(
    filters, 				# int，输出通道数
    kernel_size, 			# int或Tuple[int, int]，卷积核大小
    strides=(1, 1), 		# int或Tuple[int, int]，滑动窗口，每次卷积对原数据滑动stride个单元格
    padding='valid', 		# "valid"或"same"
    data_format=None,		# channels_last或channels_first。不指定表示是channels_last。
    dilation_rate=(1, 1), 	# int或Tuple[int, int]，膨胀系数，一个卷积核内部之间的间隔
    groups=1, 				# the number of groups in which the input is split along the channel axis
    activation=None, 		# 使用激活函数，默认不使用
    use_bias=True,			# bool，是否使用bias
    kernel_initializer='glorot_uniform', # 卷积核初始化方法
    bias_initializer='zeros',	# 偏差值初始化方法				
    kernel_regularizer=None, 	# 卷积核正则化
    bias_regularizer=None, 		# 偏差正则化
    activity_regularizer=None,	# activation函数的正则化，不太理解      
    kernel_constraint=None, 	# 卷积核的Constraint function，不太理解  
    bias_constraint=None, 		# bias的Constraint function，不太理解   
    **kwargs
)
~~~

- input shape

  - 当data_format=channels_last，则shape为$(N, H_{in},W_{in},C_{in})$
  - 当data_format=channels_first，则shape为$(N,C_{in}, H_{in},W_{in})$，和pytorch相同

- output shape

    - 当data_format=channels_last，则格式为 $(N, H_{out},W_{out},C_{out})$
    - 当data_format=channels_first，则格式为$(N,C_{out}，H_{out},W_{out})$，和pytorch相同

    设$$\mathbf {S_{in}} = \begin{bmatrix} H_{in} & W_{in} \end{bmatrix}  $$，$$ \mathbf {S_{out} }= \begin{bmatrix} H_{out} & W_{out} \end{bmatrix}  $$，则
    $$
    \mathbf {S_{out}} = 
    \begin{equation}  
    \left\{  
    \begin{array}{lcl}  
    \lfloor \frac {\mathbf { S_{in}}  - \mathbf {dilation} \circ (\mathbf {kernal\_size} -1 ) - 1} { \mathbf {stride}}  + 1 \rfloor  &  &  valid \\  
    \lfloor \frac {\mathbf { S_{in}} } { \mathbf {stride}}   \rfloor &  &  same  
    \end{array}  
    \right.
    \end{equation}
    $$

    > 上面的逻辑同样适用于Conv1d，Conv3d

- 参数个数

  $$
  (H_{kernel\_size} \times W_{kernel\_size} \times C_{in} + 1) *C_{out}
  $$

  ~~~python
  import tensorflow as tf
  
  conv2d = tf.keras.layers.Conv2D(
      filters=16, 
      kernel_size=5, 
      input_shape=[28,28,3])
  
  x = tf.ones([10, 28, 28, 3])
  y = conv2d(x)
  print(conv2d.kernel.shape)
  print(conv2d.bias.shape)
  ~~~

  ![image-20201020093743424](images/image-20201020093743424.png)

  从结果上看，参数的个数和pytorch完全相同，但维度的设置完全不同。

## padding逻辑

前文介绍了pytorch和tensorflow中关于padding逻辑，下面是代码以Conv1D为例（Conv2D逻辑是相同的），展示了其中的细节，首先看tensorflow的padding。

- valid：边缘不填充

- same：边缘用0填充

  和pytorch中不同，tersoflow中边缘的填充更加的自动化。下面以$W_{kernel\_size}$为例。

  - 左边：填充$\lfloor  \frac 1 2 (W_{kernel\_size}-1) \rfloor $个数据
  - 右边：填充$\lfloor  \frac 1 2 W_{kernel\_size} \rfloor $个数据

  总体原则是两边补0，然后实际的数据尽量位于中心位置。当$\mathbf {stride}=1$，如下图所示。

  ![image-20201019164450543](images/image-20201019164450543.png)

  当$\mathbf {stride}=2$，和上面不同在于，扣掉了一些数据。

  ![image-20201019164507736](images/image-20201019164507736.png)

验证代码如下。

~~~python
import tensorflow as tf

def conv1d(x, kernel_size=4, strides=2, padding='same'):    
    print('-'*10 + 'kernel_size={}, strides={}, padding={}'.format(kernel_size, strides, padding) + '-'*10)
    y = tf.keras.layers.Conv1D(
        filters=1, 
        kernel_size=kernel_size, 
        strides=strides, 
        padding=padding,
        input_shape=x.shape[1:], 
        kernel_initializer='ones',
        bias_constraint='zeros'
    )(x)
    print(y)
    
input_shape = (1, 9, 1)
x = tf.constant([1, 2, 3, 4, 5, 6, 7, 8, 9], shape=input_shape, dtype=tf.float32)

print('='*25 + "strides=1" + '='*25)
conv1d(x, kernel_size=5, strides=1, padding='valid')
conv1d(x, kernel_size=5, strides=1, padding='same')
conv1d(x, kernel_size=6, strides=1, padding='valid')
conv1d(x, kernel_size=6, strides=1, padding='same')

print('='*25 + "strides=2" + '='*25)
conv1d(x, kernel_size=5, strides=2, padding='valid')
conv1d(x, kernel_size=5, strides=2, padding='same')
conv1d(x, kernel_size=6, strides=2, padding='valid')
conv1d(x, kernel_size=6, strides=2, padding='same')
~~~

![image-20201019163827280](images/image-20201019163827280.png)

![image-20201019163914449](images/image-20201019163914449.png)

对于padding的添加，tensorflow更加的智能，而pytorch交给用户自己来决定。下面是pytorch的逻辑，非常相似。

![image-20201019201811447](images/image-20201019201811447.png)

~~~pytorch
import torch 

def conv1d(x, kernel_size=4, stride=2, padding=0):   
    print('-'*10 + 'kernel_size={}, stride={}, padding={}'.format(kernel_size, stride, padding) + '-'*10)
    output = torch.nn.Conv1d(
        in_channels=1,
        out_channels=1,
        kernel_size=kernel_size,
        stride=stride, 
        padding=padding
    )
    output.weight = torch.nn.Parameter(torch.ones(1, 1, kernel_size))
    output.bias = torch.nn.Parameter(torch.zeros(1))
    y = output(x)
    print(y)
    

input_shape = (1, 1, 9)
x = torch.tensor([1, 2, 3, 4, 5, 6, 7, 8, 9], dtype=torch.float)
x = x.view(input_shape)
print('='*25 + "stride=1" + '='*25)
conv1d(x, kernel_size=5, stride=1, padding=0)
conv1d(x, kernel_size=5, stride=1, padding=2)
conv1d(x, kernel_size=6, stride=1, padding=0)
conv1d(x, kernel_size=6, stride=1, padding=3)

print('='*25 + "stride=2" + '='*25)
conv1d(x, kernel_size=5, stride=2, padding=0)
conv1d(x, kernel_size=5, stride=2, padding=2)
conv1d(x, kernel_size=6, stride=2, padding=0)
conv1d(x, kernel_size=6, stride=2, padding=3)
~~~

![image-20201019201844500](images/image-20201019201844500.png)

## 实现LeNet

LeNet是Yann LeCun等人提出的卷积神经网络结构，有多个版本，一般LeNet即指LeNet-5。其结果图如下：

![image-20201019113632136](images/image-20201019113632136.png)

### pytorch实现

从上面结构图来看，不算输入层，LeNet共有7层，但有参数的只有5层，所以在pytorch中使用torch.nn定了这5层，而其它两层使用torch.nn.Fu

~~~python
import torch
from torch import nn, optim
#import torch.nn.functional as F
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision import datasets
#from logger import Logger

# 定义超参数
batch_size = 128        # 批的大小
learning_rate = 1e-2    # 学习率
num_epoches = 20        # 遍历训练集的次数

# 数据类型转换，转换成numpy类型
#def to_np(x):
#    return x.cpu().data.numpy()


# 下载训练集 MNIST 手写数字训练集
train_dataset = datasets.MNIST(
    root='./data', train=True, transform=transforms.ToTensor(), download=True)

test_dataset = datasets.MNIST(
    root='./data', train=False, transform=transforms.ToTensor())

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)


# 定义 Convolution Network 模型
class Cnn(nn.Module):
    def __init__(self, in_dim, n_class):
        super(Cnn, self).__init__()    # super用法:Cnn继承父类nn.Model的属性，并用父类的方法初始化这些属性
        self.conv = nn.Sequential(     #padding=2保证输入输出尺寸相同(参数依次是:输入深度，输出深度，ksize，步长，填充)
            nn.Conv2d(in_dim, 6, 5, stride=1, padding=2),
            nn.ReLU(True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(6, 16, 5, stride=1, padding=0),
            nn.ReLU(True), 
            nn.MaxPool2d(2, 2))

        self.fc = nn.Sequential(
            nn.Linear(400, 120), 
            nn.Linear(120, 84), 
            nn.Linear(84, n_class))

    def forward(self, x):
        out = self.conv(x)
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        return out


model = Cnn(1, 10)  # 图片大小是28x28,输入深度是1，最终输出的10类
use_gpu = torch.cuda.is_available()  # 判断是否有GPU加速
if use_gpu:
    model = model.cuda()

# 定义loss和optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=learning_rate)

#logger = Logger('./logs')
# 开始训练
for epoch in range(num_epoches):
    print('epoch {}'.format(epoch + 1))      # .format为输出格式，formet括号里的即为左边花括号的输出
    print('*' * 10)
    running_loss = 0.0
    running_acc = 0.0
    for i, data in enumerate(train_loader, 1):
        img, label = data
        # cuda
        if use_gpu:
            img = img.cuda()
            label = label.cuda()
        img = Variable(img)
        label = Variable(label)
        # 向前传播
        out = model(img)
        loss = criterion(out, label)
        running_loss += loss.item() * label.size(0)
        _, pred = torch.max(out, 1)
        num_correct = (pred == label).sum()
        accuracy = (pred == label).float().mean()
        running_acc += num_correct.item()
        # 向后传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        """
        # ========================= Log ======================
        step = epoch * len(train_loader) + i
        # (1) Log the scalar values
        info = {'loss': loss.data[0], 'accuracy': accuracy.data[0]}

        for tag, value in info.items():
            logger.scalar_summary(tag, value, step)

        # (2) Log values and gradients of the parameters (histogram)
        for tag, value in model.named_parameters():
            tag = tag.replace('.', '/')
            logger.histo_summary(tag, to_np(value), step)
            logger.histo_summary(tag + '/grad', to_np(value.grad), step)

        # (3) Log the images
        info = {'images': to_np(img.view(-1, 28, 28)[:10])}

        for tag, images in info.items():
            logger.image_summary(tag, images, step)
        if i % 300 == 0:
            print('[{}/{}] Loss: {:.6f}, Acc: {:.6f}'.format(
                epoch + 1, num_epoches, running_loss / (batch_size * i),
                running_acc / (batch_size * i)))
        """
    print('Finish {} epoch, Loss: {:.6f}, Acc: {:.6f}'.format(
        epoch + 1, running_loss / (len(train_dataset)), running_acc / (len(train_dataset))))
    model.eval()
    eval_loss = 0
    eval_acc = 0
    for data in test_loader:
        img, label = data
        if use_gpu:
            img = Variable(img, volatile=True).cuda()
            label = Variable(label, volatile=True).cuda()
        else:
            img = Variable(img, volatile=True)
            label = Variable(label, volatile=True)
        out = model(img)
        loss = criterion(out, label)
        eval_loss += loss.item() * label.size(0)
        _, pred = torch.max(out, 1)
        num_correct = (pred == label).sum()
        eval_acc += num_correct.item()
    print('Test Loss: {:.6f}, Acc: {:.6f}'.format(eval_loss / (len(
        test_dataset)), eval_acc / (len(test_dataset))))
    print()

# 保存模型
torch.save(model.state_dict(), './cnn.pth')
~~~



## 参考

- 

