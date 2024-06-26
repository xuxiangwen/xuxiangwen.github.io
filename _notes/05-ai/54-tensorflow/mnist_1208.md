---
title: MNIST
categories: deep-learning
date: 2020-10-26
---
[MNIST](https://eipi10.cn/others/2020/10/22/dataset/)（Mixed National Institute of Standards and Technology）数据集是著名的手写数字数据集，被誉为数据科学领域的`果蝇`。本文使用pytorch和tensorflow实现对MNIST数据集进行分类，先从经典神经网络开始，然后使用LeNet，最后还尝试了用相同的算法对[Fashion MNIST](https://eipi10.cn/others/2020/10/22/dataset/#fashion-mnist)数据集进行分类。

## 经典神经网络

首先，尝试用经典的神经网络来进行分类。

### pytorch

~~~python
import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import time
import torch
import torchvision
import torch.nn.functional as F
from torch import nn, optim
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision import datasets

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)


class TaskTime:
    def __init__(self, task_name, show_start=False):
        self.show_start = show_start
        self.task_name = task_name
        self.start_time = time.time()

    def elapsed_time(self):
        return time.time()-self.start_time

    def __enter__(self):
        if self.show_start:
            logging.info('start {}'.format(self.task_name))
        return self;

    def __exit__(self, exc_type, exc_value, exc_tb):
        time.sleep(0.5)
        logging.info('finish {} [elapsed time: {:.2f} seconds]'.format(self.task_name, self.elapsed_time()))

    
def compute_loss_accuarcy(net, loader, criterion, use_cuda=False, max_load_times=0):
    num_correct = 0
    total = 0
    total_loss = 0
    with torch.no_grad():
        for i, data in enumerate(loader):
            if max_load_times>0 and i>=max_load_times: break
            inputs, labels = data
            _, loss, correct = forward(net, inputs, labels, criterion, use_cuda) 
            total += labels.size(0)
            total_loss += loss*labels.size(0)
            num_correct += correct    

    return total_loss/total, num_correct/total

def forward(net, inputs, labels, criterion, use_cuda=False):   
    if use_cuda and  torch.cuda.is_available(): 
        net = net.cuda()
        criterion = criterion.cuda()
        inputs = inputs.cuda()
        labels = labels.cuda()
    outputs = net(inputs)
    loss = criterion(outputs, labels)   
    _, predicted = torch.max(outputs.data, 1)
    num_correct = (predicted == labels).sum().item()
    num_total = labels.size(0)     
    return outputs, loss, num_correct        
    
def train(net, criterion, optimizer, trainloader, validationloader, epochs=2, use_cuda=False):  
        
    train_loss_list = []
    train_accuracy_list = []
    val_loss_list = []
    val_accuracy_list = []      
    
    for epoch in range(epochs):         
        train_loss = 0.0
        train_num_correct = 0
        train_total = 0                   
        
        for i, data in enumerate(trainloader, 0):
            inputs, labels = data   
            # 正向传播
            _, loss, correct = forward(net, inputs, labels, criterion, use_cuda)  
            
            train_loss += loss.item()*labels.size(0)
            train_num_correct += correct
            train_total += labels.size(0)     
            
            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
                        
            if i % 50 == 49:        
                sys.stdout.write('\r[epoch %2d/%2d %5d] loss: %.3f, accuracy: %.3f' % 
                                  (epoch + 1, epochs, i+1, train_loss/train_total, train_num_correct/train_total))                
                train_loss = 0.0
                train_num_correct = 0
                train_total = 0                   
                                                                                
        train_loss, train_accuracy = compute_loss_accuarcy(net, trainloader, criterion, 
                                                           use_cuda=True, max_load_times=50)   
        val_loss, val_accuracy = compute_loss_accuarcy(net, validationloader, criterion, 
                                                       use_cuda=True, max_load_times=50)
        
        train_loss_list.append(train_loss)
        train_accuracy_list.append(train_accuracy)
        val_loss_list.append(val_loss)
        val_accuracy_list.append(val_accuracy)         
        
        sys.stdout.write('\r[epoch %2d/%2d] loss: %.3f, accuracy: %.3f, val_loss: %.3f, val_accuracy: %.3f \n' %
                          (epoch + 1, epochs, train_loss, train_accuracy, val_loss, val_accuracy))
         

    return train_loss_list, train_accuracy_list, val_loss_list, val_accuracy_list
                
class NN(nn.Module):
    def __init__(self, in_dim=1, n_class=10, p=0.2):
        super(NN, self).__init__()    

        self.fc1 = nn.Linear(28*28, 128)  
        self.fc2 = nn.Linear(128, n_class)
        
        self.drop_layer = nn.Dropout(p=p)
          
    def forward(self, x):
        x = x.view(x.size()[0], -1)
        x = F.relu(self.fc1(x))
        x = self.drop_layer(x)
        x = self.fc2(x)
        return x
~~~

下面是数据加载的代码。

~~~python
def torch_mnist_extract_data(dataset='mnist', classes=None):
    with TaskTime('获取数据', True):
        transform = transforms.Compose(
            [transforms.ToTensor(),
             transforms.Normalize(mean=(0.5), std=(0.5))])
        data_path = os.path.join(os.path.expanduser('~'), '.pytorch/datasets') 
        if not os.path.exists(data_path): os.makedirs(data_path)
        if dataset=='mnist':
            trainset = torchvision.datasets.MNIST(root=os.path.join(data_path, dataset), train=True,
                                                  download=True, transform=transform)
            trainloader = torch.utils.data.DataLoader(trainset, batch_size=32,
                                                      shuffle=True, num_workers=2)

            testset = torchvision.datasets.MNIST(root=os.path.join(data_path, dataset), train=False,
                                                 download=True, transform=transform)
            testloader = torch.utils.data.DataLoader(testset, batch_size=32,
                                                     shuffle=False, num_workers=2)
        else:
            trainset = torchvision.datasets.FashionMNIST(root=os.path.join(data_path, dataset), train=True,
                                                          download=True, transform=transform)
            trainloader = torch.utils.data.DataLoader(trainset, batch_size=32,
                                                      shuffle=True, num_workers=2)

            testset = torchvision.datasets.FashionMNIST(root=os.path.join(data_path, dataset), train=False,
                                                        download=True, transform=transform)
            testloader = torch.utils.data.DataLoader(testset, batch_size=32,
                                                     shuffle=True, num_workers=2)           

    with TaskTime('显示图片示例', True):
        plt.rcParams['figure.figsize'] = (12.0, 1.5) 
        def imshow(img):
            img = img / 2 + 0.5     # unnormalize
            npimg = img.numpy()
            plt.imshow(np.transpose(npimg, (1, 2, 0)))
            plt.show()

        # get some random training images
        dataiter = iter(trainloader)
        images, labels = dataiter.next()
        print(images.shape)

        # show images
        print(' '.join('%5s' %  labels[j].item() if classes is None else classes[labels[j].item()] for j in range(8)))
        imshow(torchvision.utils.make_grid(images[0:8]))

    return trainset, trainloader, testset, testloader

trainset, trainloader, testset, testloader = torch_mnist_extract_data()    
   
~~~

![image-20201101153954004](images/image-20201101153954004.png)

接下来是模型创建，模型训练，保存加载，以及模型评估的代码。

~~~python
def torch_train_evaluate(net, epochs=10, save_model=False, model_file_name='torch_nn.pth'):                   
    with TaskTime('显示参数', True):
         # 由于存在bias，所以每一层都有两个参数张量，共有10个参数张量。
        params = list(net.parameters())
        print(len(params))
        for param in params:
            print(param.size())  

    with TaskTime('模型训练', True):
        criterion = nn.CrossEntropyLoss()
        # optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)      # Adam优化的速度比SGD明显要快
        optimizer = optim.Adam(net.parameters(), lr=0.001, betas=(0.9, 0.999), eps=1e-08, weight_decay=0, amsgrad=False)
        _, train_accuracy_list, _, val_accuracy_list = train(
            net, criterion, optimizer, trainloader, testloader, epochs=epochs, use_cuda=True)

    if save_model:  
        with TaskTime('保存，加载模型', True):
            model_root_path = os.path.join(os.path.expanduser('~'), '.pytorch/model') 
            if not os.path.exists(model_root_path): os.makedirs(model_root_path)
            model_path = os.path.join(model_root_path, model_file_name)
            torch.save(net.state_dict(), model_path) 
            net.load_state_dict(torch.load(model_path))     

    with TaskTime('评估模型', True):
        plt.figure(figsize=(8, 3))
        plt.plot(train_accuracy_list, label='accuracy')
        plt.plot(val_accuracy_list, label = 'val_accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.ylim([0, 1])
        plt.legend(loc='lower right')          
        
        _, train_accuracy = compute_loss_accuarcy(net, trainloader, criterion, use_cuda=True)   
        _, test_accuracy = compute_loss_accuarcy(net, testloader, criterion, use_cuda=True)
        print('Train Accuracy: {:0.3f}, Test Accuracy: {:0.3f}'.format(train_accuracy, test_accuracy)) 
        
with TaskTime('创建模型', True):      
    net = NN(in_dim=1, n_class=10)
    print(net)

torch_train_evaluate(net, epochs=5, save_model=True, model_file_name='torch_nn.pth')
~~~

![image-20201101154732934](images/image-20201101154732934.png)

Accuracy超过95%，应该来说，效果非常不错。

### tensorflow

~~~python
import logging
import os
import tensorflow as tf
import time
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)

# 设置GPU内存使用上限
gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
print(gpus)
tf.config.experimental.set_virtual_device_configuration(
    gpus[0],
    [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024)]
)

def neural_network():
    model = models.Sequential()
    model.add(layers.Flatten(input_shape=(28, 28)))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(10))    
    return model
~~~

然后加载数据。

~~~python
def tf_mnist_extract_data(dataset='mnist', classes=None):
    with TaskTime('获取数据', True):
        # 默认的保存路径是~/.keras/datasets/
        if dataset=='mnist':
            (train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data()
        else:
            (train_images, train_labels), (test_images, test_labels) = datasets.fashion_mnist.load_data()

        # Normalize pixel values to be between 0 and 1
        train_images, test_images = train_images / 255.0, test_images / 255.0     

        print(train_images.shape, train_labels.shape, train_images.shape, test_labels.shape)
        print(type(train_images), type(train_labels.shape))

    with TaskTime('显示图片示例', True):

        plt.figure(figsize=(10,2))
        for i in range(5):
            plt.subplot(1,5,i+1)
            plt.xticks([])
            plt.yticks([])
            plt.grid(False)
            plt.imshow(train_images[i], cmap='gray', interpolation='none')
            # The CIFAR labels happen to be arrays, 
            # which is why you need the extra index
            plt.xlabel(train_labels[i] if classes is None else classes[train_labels[i]])
        plt.show()
    
    return train_images, train_labels, test_images, test_labels

train_images, train_labels, test_images, test_labels = tf_mnist_extract_data()
~~~

![image-20201101154906118](images/image-20201101154906118.png)

接下来是模型创建，模型训练，保存加载，以及模型评估的代码。

~~~python
def tf_train_evaluate(model, epochs=2, save_model=False, model_file_name='tf_nn.h5'):   
    with TaskTime('显示参数', True):
        model.summary()

    with TaskTime('模型训练', True):    
        model.compile(optimizer='adam',
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy'])
        history = model.fit(train_images, train_labels, epochs=epochs, batch_size=32,
                            validation_data=(test_images, test_labels))

    if save_model:
        with TaskTime('保存，加载模型', True): 
            model_root_path = os.path.join(os.path.expanduser('~'), '.keras/model') 
            if not os.path.exists(model_root_path): os.makedirs(model_root_path)
            model_path = os.path.join(model_root_path, model_file_name)
            model.save(model_path) 
            model = tf.keras.models.load_model(model_path)  

    with TaskTime('评估模型', True): 
        plt.figure(figsize=(8, 3))
        plt.plot(history.history['accuracy'], label='accuracy')
        plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.ylim([0.5, 1])
        plt.legend(loc='lower right')

        train_loss, train_acc = model.evaluate(train_images,  train_labels, verbose=2)
        test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
        print('Train Accuracy: {:0.1f}%, Test Accuracy: {:0.1f}%'.format(100 * train_acc, 100*test_acc)) 

with TaskTime('创建模型', True): 
    model = neural_network( )

tf_train_evaluate(model, epochs=5, save_model=True, model_file_name='tf_nn.h5')
~~~

![image-20201101155159974](images/image-20201101155159974.png)

Accuracy比pytorch明显更加一点，超过97%，效果非常不错。

## LeNet模型

下面尝试用[LeNet5](https://eipi10.cn/deep-learning/2020/10/23/lenet/)来实现，看看是不是还能有提高。下面是LeNet5的结构图。

![image-20201019113632136](images/image-20201019113632136.png)

### pytorch

在LeNet5中，输入层是$32\times32$的图片，而MNIST是$28\times28$的图片，为了保持模型的结构不变，在第一个卷积积增加一个参数padding=2。

~~~python
class LeNet(nn.Module):
    def __init__(self, in_dim=1, n_class=10):
        super(LeNet, self).__init__()    

        self.conv1 = nn.Conv2d(in_dim, 6, 5, padding=2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)  
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, n_class)        
        
    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), 2)
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(x.size()[0], -1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
~~~

下面来训练LeNet。

~~~python
with TaskTime('创建模型', True):      
    net = LeNet(in_dim=1, n_class=10)
    print(net)

torch_train_evaluate(net, epochs=5)
~~~

![image-20201101155427083](images/image-20201101155427083.png)

经过5个epoch，accuracy有一些提高，能达到将近99%，非常理想。

### tensorflow

同样为了保持模型的结构不变，设置一个参数padding='same'，另外input_shape改成了(28, 28, in_dim)。

~~~python
def lenet(in_dim=1, n_class=10):
    model = models.Sequential()
    model.add(layers.Conv2D(6, (5, 5), activation='relu', padding='same', input_shape=(28, 28, in_dim)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(16, (5, 5), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(120, activation='relu'))
    model.add(layers.Dense(84, activation='relu'))
    model.add(layers.Dense(n_class))    
    return model
~~~

由于采用卷积神经网络，需要有channel，所以对数据增加一个维度。

~~~python
train_images = tf.expand_dims(train_images, axis=-1)
test_images = tf.expand_dims(test_images, axis=-1)
~~~

下面来训练lenet。

~~~python
with TaskTime('创建模型', True): 
    model = lenet(in_dim=1, n_class=10)

tf_train_evaluate(model, epochs=5)
~~~

![image-20201101155627164](images/image-20201101155627164.png)

同样，比起经典神经网络，accuracy又提高了一点，接近99%，非常好。

## Fashion MNIST

对于MNIST数据集，无论采用经典神经网络还是LeNet都能取得不错的效果，LeNet收敛速度更快，Accuracy也高一点。下面来尝试一下[Fashion MNIST](https://eipi10.cn/others/2020/10/22/dataset/#fashion-mnist)数据集，这个数据集和MNIST的结构完全相同，代码可以几乎不用修改。

### pytorch

首先下载数据。

~~~python
classes=['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal','Shirt', 'Sneaker', 'Bag', 'Ankle boot']
trainset, trainloader, testset, testloader = torch_mnist_extract_data(dataset='fashion-mnist', classes=classes) 
~~~

![image-20201101155942093](images/image-20201101155942093.png)

接下来开始训练模型，第一个看经典的神经网络。

~~~python
with TaskTime('创建模型', True):      
    net = NN(in_dim=1, n_class=10)
    print(net)

torch_train_evaluate(net, epochs=5)
~~~

![image-20201101155922563](images/image-20201101155922563.png)

Accuracy只有85%，下面再来看LeNet。

~~~python
with TaskTime('创建模型', True):      
    net = LeNet(in_dim=1, n_class=10)
    print(net)

torch_train_evaluate(net, epochs=5)
~~~

![image-20201101160338728](images/image-20201101160338728.png)

Accuracy提高到了89%，不错。下面来看一种改进的LeNet。它增加了一层卷积，并大大增加了卷积的深度，同时减少了一层全连接层（或许可以减少一些过拟合）。

~~~python
class LeNet1(nn.Module):
    def __init__(self, in_dim=1, n_class=10):
        super(LeNet1, self).__init__()    

        self.conv1 = nn.Conv2d(in_dim, 32, 3, padding=2)
        self.conv2 = nn.Conv2d(32, 64, 3)
        self.conv3 = nn.Conv2d(64, 64, 3)
        self.fc1 = nn.Linear(64 * 4 * 4, 64)  
        self.fc2 = nn.Linear(64, n_class)        
        
    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), 2)
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = F.relu(self.conv3(x))
        x = x.view(x.size()[0], -1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
    
with TaskTime('创建模型', True):      
    net = LeNet1(in_dim=1, n_class=10)
    print(net)

torch_train_evaluate(net, epochs=5)
~~~

![image-20201101161011299](images/image-20201101161011299.png)

Accuracy继续提高到了91%。增加卷积的深度，看来还是有用的。

### tensorflow

首先也是下载数据。

~~~python
classes=['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal','Shirt', 'Sneaker', 'Bag', 'Ankle boot']
train_images, train_labels, test_images, test_labels = tf_mnist_extract_data(dataset='fashion-mnist', classes=classes)
~~~

![image-20201101161100232](images/image-20201101161100232.png)

接下来开始训练模型，第一个看经典的神经网络。

~~~python
with TaskTime('创建模型', True): 
    model = neural_network( )

tf_train_evaluate(model, epochs=5)
~~~

![image-20201101161204018](images/image-20201101161204018.png)

Accuracy只有87%左右，下面再来看LeNet。别忘了由于采用卷积神经网络，需要有channel，所以对数据增加一个维度。

~~~python
train_images = tf.expand_dims(train_images, axis=-1)
test_images = tf.expand_dims(test_images, axis=-1)

# 下面两行代码可以实现上面相同的逻辑
# train_images = train_images[..., np.newaxis]
# test_images = test_images[..., np.newaxis]
~~~

训练代码如下：

~~~python
with TaskTime('创建模型', True): 
    model = lenet(in_dim=1, n_class=10)

tf_train_evaluate(model, epochs=5)
~~~

![image-20201101161431198](images/image-20201101161431198.png)

和pytorch一样，Accuracy同样提高到了89%。然后看改进的LeNet。它增加了一层卷积，并大大增加了卷积的深度，同时减少了一层全连接层（或许可以减少一些过拟合）。

~~~python
def lenet1(in_dim=1, n_class=10):
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', padding="same", input_shape=(28, 28, in_dim)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))    
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(n_class))    
    return model

with TaskTime('创建模型', True): 
    model = lenet1(in_dim=1, n_class=10)

tf_train_evaluate(model, epochs=5)
~~~

![image-20201101161639102](images/image-20201101161639102.png)

同样，Accuracy也提高到了91%。如果再训练5个epoch，得到结果如下。

~~~python
tf_train_evaluate(model, epochs=5)
~~~

![image-20201101161830039](images/image-20201101161830039.png)

准确率还是91%多，但过拟合明显严重多了，看来要继续改进模型结构才可以啊。

## 总结

归纳上面的模型训练结果，可以得出以下几个结论。

- LeNet比经典的神经网络参数要少，模型收敛更快，准确率明显提升。
- MNIST数据集过于简单了，很简单的算法也能轻易取得99%的准确率。建议采用Fashion MNIST作为替代。
- 增加卷积的深度，对于准确率的提升是有明显作用的。
- 本文中，对于Fashion MNIST最好只能取得91%的准确率，还需要采用新的模型结构才能继续提升。

## 参考

- [TensorFlow 2 quickstart for beginners](https://www.tensorflow.org/tutorials/quickstart/beginner)

## 历史

- 2020-10-26：初始版本
- 2020-10-28：采用相同算法，对Fashion Mnist数据集进行分类
- 2020-11-01：pytorch训练时，增加了validation accuaracy。