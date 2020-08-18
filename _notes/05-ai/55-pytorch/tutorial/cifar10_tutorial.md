```{.python .input  n=1}
import sys

base_path = '/tf/eipi10/qbz95'
sys.path.append(base_path)

from qbz95 import config
import pandas as pd
config = config.get_config('jupyter')
pd.set_option('display.width', 1000)

%matplotlib inline

# 代码自动重新加载
%load_ext autoreload
%autoreload 2

# #当module有新的方法的时候，需要运行下面方法。
# %reload_ext autoreload 

from qbz95.ml3.utils import util
```

```{.json .output n=1}
[
 {
  "name": "stderr",
  "output_type": "stream",
  "text": "2020-01-13 07:45:05,977: INFO: deployment = jupyter\n2020-01-13 07:45:05,978: INFO: base_path = /tf/eipi10/qbz95/qbz95\n2020-01-13 07:45:05,980: INFO: data_path = /tf/eipi10/qbz95/data\n2020-01-13 07:45:06,503: INFO: deployment = jupyter\n2020-01-13 07:45:06,504: INFO: base_path = /tf/eipi10/qbz95/qbz95\n2020-01-13 07:45:06,505: INFO: data_path = /tf/eipi10/qbz95/data\n"
 }
]
```

```{.python .input  n=2}
%matplotlib inline
```


Training a Classifier
=====================

This is it. You have seen how to define neural networks, compute loss and make
updates to the weights of the network.

Now you might be thinking,

What about data?
----------------

Generally, when you have to deal with image, text, audio or video data,
you can use standard python packages that load data into a numpy array.
Then you can convert this array into a ``torch.*Tensor``.

-  For images, packages such as Pillow, OpenCV are useful
-  For audio, packages such as scipy and librosa
-  For text, either raw Python or Cython based loading, or NLTK and
   SpaCy are useful

Specifically for vision, we have created a package called
``torchvision``, that has data loaders for common datasets such as
Imagenet, CIFAR10, MNIST, etc. and data transformers for images, viz.,
``torchvision.datasets`` and ``torch.utils.data.DataLoader``.

This provides a huge convenience and avoids writing boilerplate code.

For this tutorial, we will use the CIFAR10 dataset.
It has the classes: ‘airplane’, ‘automobile’, ‘bird’, ‘cat’, ‘deer’,
‘dog’, ‘frog’, ‘horse’, ‘ship’, ‘truck’. The images in CIFAR-10 are of
size 3x32x32, i.e. 3-channel color images of 32x32 pixels in size.

![cifar10](https://pytorch.org/tutorials/_images/cifar10.png)

   cifar10


Training an image classifier
----------------------------

We will do the following steps in order:

1. Load and normalizing the CIFAR10 training and test datasets using
   ``torchvision``
2. Define a Convolutional Neural Network
3. Define a loss function
4. Train the network on the training data
5. Test the network on the test data


### 1. Loading and normalizing CIFAR10

Using ``torchvision``, it’s extremely easy to load CIFAR10.


```{.python .input  n=3}
import torch
import torchvision
import torchvision.transforms as transforms
```

The output of torchvision datasets are PILImage images of range [0, 1].
We transform them to Tensors of normalized range [-1, 1].
<div class="alert alert-info"><h4>Note</h4><p>If running on Windows and you get
a BrokenPipeError, try setting
    the num_worker of torch.utils.data.DataLoader() to 0.</p></div>


```{.python .input  n=4}
transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                        download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=4,
                                          shuffle=True, num_workers=2)

testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                       download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=4,
                                         shuffle=False, num_workers=2)

classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
```

```{.json .output n=4}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "Files already downloaded and verified\nFiles already downloaded and verified\n"
 }
]
```

Let us show some of the training images, for fun.


```{.python .input  n=5}
import matplotlib.pyplot as plt
import numpy as np

# functions to show an image


def imshow(img):
    img = img / 2 + 0.5     # unnormalize
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()


# get some random training images
dataiter = iter(trainloader)
images, labels = dataiter.next()

# show images
imshow(torchvision.utils.make_grid(images))
# print labels
print(' '.join('%5s' % classes[labels[j]] for j in range(4)))
```

```{.json .output n=5}
[
 {
  "data": {
   "image/png": "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\n",
   "text/plain": "<Figure size 432x288 with 1 Axes>"
  },
  "metadata": {
   "needs_background": "light"
  },
  "output_type": "display_data"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "  dog   cat   dog   car\n"
 }
]
```

###  2. Define   Convolutional Neural Network

Copy the neural network from the Neural Networks section before and modify it to
take 3-channel images (instead of 1-channel images as it was defined).


```{.python .input  n=6}
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


net = Net()
print(net)
```

```{.json .output n=6}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "Net(\n  (conv1): Conv2d(3, 6, kernel_size=(5, 5), stride=(1, 1))\n  (pool): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)\n  (conv2): Conv2d(6, 16, kernel_size=(5, 5), stride=(1, 1))\n  (fc1): Linear(in_features=400, out_features=120, bias=True)\n  (fc2): Linear(in_features=120, out_features=84, bias=True)\n  (fc3): Linear(in_features=84, out_features=10, bias=True)\n)\n"
 }
]
```

```{.python .input  n=7}
params = list(net.parameters())
print(len(params))
# print(params[0].size())  # conv1's .weight
for param in params:
    print(param.size())
```

```{.json .output n=7}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "10\ntorch.Size([6, 3, 5, 5])\ntorch.Size([6])\ntorch.Size([16, 6, 5, 5])\ntorch.Size([16])\ntorch.Size([120, 400])\ntorch.Size([120])\ntorch.Size([84, 120])\ntorch.Size([84])\ntorch.Size([10, 84])\ntorch.Size([10])\n"
 }
]
```

### 3. Define a Loss function and optimizer

Let's use a Classification Cross-Entropy loss and SGD with momentum.


```{.python .input  n=8}
import torch.optim as optim

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
```

4. Train the network
^^^^^^^^^^^^^^^^^^^^

This is when things start to get interesting.
We simply have to loop over our data iterator, and feed the inputs to the
network and optimize.


```{.python .input  n=25}
def train(net, criterion, trainloader, use_cuda=False):
    cuda_run = None
    if use_cuda and  torch.cuda.is_available():
        cuda_run = True
        net = net.cuda()
        criterion = criterion.cuda()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

    for epoch in range(2):  # loop over the dataset multiple times
        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = data            
            if cuda_run:
                inputs = inputs.cuda()
                labels = labels.cuda()

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            if i % 2000 == 1999:    # print every 2000 mini-batches
                print('[%d, %5d] loss: %.3f' %
                      (epoch + 1, i + 1, running_loss / 2000))
                running_loss = 0.0

```

```{.python .input}

```

```{.python .input  n=13}
net = Net()
with util.TaskTime('training', True):
    train(net, criterion, trainloader)
```

```{.json .output n=13}
[
 {
  "name": "stderr",
  "output_type": "stream",
  "text": "2020-01-13 07:50:09,048: INFO: start training\n"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "[1,  2000] loss: 2.130\n[1,  4000] loss: 1.831\n[1,  6000] loss: 1.640\n[1,  8000] loss: 1.572\n[1, 10000] loss: 1.509\n[1, 12000] loss: 1.459\n[2,  2000] loss: 1.387\n[2,  4000] loss: 1.366\n[2,  6000] loss: 1.364\n[2,  8000] loss: 1.322\n[2, 10000] loss: 1.295\n[2, 12000] loss: 1.298\n"
 },
 {
  "name": "stderr",
  "output_type": "stream",
  "text": "2020-01-13 07:52:31,291: INFO: finish training [elapsed time: 142.24 seconds]\n"
 }
]
```

使用cuda计算，速度从140多秒变成100多秒。好像也没快多少啊.
如后文所说，是网络太小了，导致不明显。另外一个原因是后台看到大概使用了70%的cpu,aa00有20核，也就是说14个cpu参与了的计算。

```{.python .input  n=26}
net = Net()
with util.TaskTime('training', True):
    train(net, criterion, trainloader, True)   
```

```{.json .output n=26}
[
 {
  "name": "stderr",
  "output_type": "stream",
  "text": "2020-01-13 08:48:30,498: INFO: start training\n"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "[1,  2000] loss: 2.233\n[1,  4000] loss: 1.943\n[1,  6000] loss: 1.740\n[1,  8000] loss: 1.606\n[1, 10000] loss: 1.517\n[1, 12000] loss: 1.481\n[2,  2000] loss: 1.382\n[2,  4000] loss: 1.373\n[2,  6000] loss: 1.351\n[2,  8000] loss: 1.303\n[2, 10000] loss: 1.285\n[2, 12000] loss: 1.290\n"
 },
 {
  "name": "stderr",
  "output_type": "stream",
  "text": "2020-01-13 08:50:13,481: INFO: finish training [elapsed time: 102.98 seconds]\n"
 }
]
```

Let's quickly save our trained model:


```{.python .input  n=27}
PATH = './cifar_net.pth'
torch.save(net.state_dict(), PATH)
```

See `here <https://pytorch.org/docs/stable/notes/serialization.html>`_
for more details on saving PyTorch models.

5. Test the network on the test data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We have trained the network for 2 passes over the training dataset.
But we need to check if the network has learnt anything at all.

We will check this by predicting the class label that the neural network
outputs, and checking it against the ground-truth. If the prediction is
correct, we add the sample to the list of correct predictions.

Okay, first step. Let us display an image from the test set to get familiar.


```{.python .input  n=28}
dataiter = iter(testloader)
images, labels = dataiter.next()

# print images
imshow(torchvision.utils.make_grid(images))
print('GroundTruth: ', ' '.join('%5s' % classes[labels[j]] for j in range(4)))
```

```{.json .output n=28}
[
 {
  "data": {
   "image/png": "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\n",
   "text/plain": "<Figure size 432x288 with 1 Axes>"
  },
  "metadata": {
   "needs_background": "light"
  },
  "output_type": "display_data"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "GroundTruth:    cat  ship  ship plane\n"
 }
]
```

Next, let's load back in our saved model (note: saving and re-loading the model
wasn't necessary here, we only did it to illustrate how to do so):


```{.python .input  n=29}
net = Net()
net.load_state_dict(torch.load(PATH))
```

```{.json .output n=29}
[
 {
  "data": {
   "text/plain": "<All keys matched successfully>"
  },
  "execution_count": 29,
  "metadata": {},
  "output_type": "execute_result"
 }
]
```

Okay, now let us see what the neural network thinks these examples above are:


```{.python .input  n=30}
outputs = net(images)
```

The outputs are energies for the 10 classes.
The higher the energy for a class, the more the network
thinks that the image is of the particular class.
So, let's get the index of the highest energy:


```{.python .input  n=31}
_, predicted = torch.max(outputs, 1)

print('Predicted: ', ' '.join('%5s' % classes[predicted[j]]
                              for j in range(4)))
```

```{.json .output n=31}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "Predicted:   bird   car   car plane\n"
 }
]
```

The results seem pretty good.

Let us look at how the network performs on the whole dataset.


```{.python .input  n=32}
correct = 0
total = 0
with torch.no_grad():
    for data in testloader:
        images, labels = data
        outputs = net(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print('Accuracy of the network on the 10000 test images: %d %%' % (
    100 * correct / total))
```

```{.json .output n=32}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "Accuracy of the network on the 10000 test images: 55 %\n"
 }
]
```

That looks way better than chance, which is 10% accuracy (randomly picking
a class out of 10 classes).
Seems like the network learnt something.

Hmmm, what are the classes that performed well, and the classes that did
not perform well:


```{.python .input  n=34}
class_correct = list(0. for i in range(10))
class_total = list(0. for i in range(10))
with torch.no_grad():
    for data in testloader:
        images, labels = data
        outputs = net(images)
        _, predicted = torch.max(outputs, 1)
        c = (predicted == labels).squeeze()
        for i in range(4):
            label = labels[i]
            class_correct[label] += c[i].item()
            class_total[label] += 1

for i in range(10):
    print('Accuracy of %5s : %2d %%' % (
        classes[i], 100 * class_correct[i] / class_total[i]))
```

```{.json .output n=34}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "tensor([3, 5, 1, 7])\nAccuracy of plane : 57 %\nAccuracy of   car : 72 %\nAccuracy of  bird : 45 %\nAccuracy of   cat : 29 %\nAccuracy of  deer : 36 %\nAccuracy of   dog : 48 %\nAccuracy of  frog : 82 %\nAccuracy of horse : 63 %\nAccuracy of  ship : 56 %\nAccuracy of truck : 66 %\n"
 }
]
```

Okay, so what next?

How do we run these neural networks on the GPU?

Training on GPU
----------------
Just like how you transfer a Tensor onto the GPU, you transfer the neural
net onto the GPU.

Let's first define our device as the first visible cuda device if we have
CUDA available:


```{.python .input  n=35}
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Assuming that we are on a CUDA machine, this should print a CUDA device:

print(device)
```

```{.json .output n=35}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "cuda:0\n"
 }
]
```

The rest of this section assumes that ``device`` is a CUDA device.

Then these methods will recursively go over all modules and convert their
parameters and buffers to CUDA tensors:

.. code:: python

    net.to(device)


Remember that you will have to send the inputs and targets at every step
to the GPU too:

.. code:: python

        inputs, labels = data[0].to(device), data[1].to(device)

Why dont I notice MASSIVE speedup compared to CPU? Because your network
is really small.

**Exercise:** Try increasing the width of your network (argument 2 of
the first ``nn.Conv2d``, and argument 1 of the second ``nn.Conv2d`` –
they need to be the same number), see what kind of speedup you get.

**Goals achieved**:

- Understanding PyTorch's Tensor library and neural networks at a high level.
- Train a small neural network to classify images

Training on multiple GPUs
-------------------------
If you want to see even more MASSIVE speedup using all of your GPUs,
please check out :doc:`data_parallel_tutorial`.

Where do I go next?
-------------------

-  :doc:`Train neural nets to play video games
</intermediate/reinforcement_q_learning>`
-  `Train a state-of-the-art ResNet network on imagenet`_
-  `Train a face generator using Generative Adversarial Networks`_
-  `Train a word-level language model using Recurrent LSTM networks`_
-  `More examples`_
-  `More tutorials`_
-  `Discuss PyTorch on the Forums`_
-  `Chat with other users on Slack`_




Exercises
-------------------

Try increasing the width of your network (argument 2 of the first nn.Conv2d, and
argument 1 of the second nn.Conv2d – they need to be the same number), see what
kind of speedup you get

```{.python .input  n=50}

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(16, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


net = Net()
print(net)

```

```{.json .output n=50}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "Net(\n  (conv1): Conv2d(3, 16, kernel_size=(5, 5), stride=(1, 1))\n  (pool): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)\n  (conv2): Conv2d(16, 16, kernel_size=(5, 5), stride=(1, 1))\n  (fc1): Linear(in_features=400, out_features=120, bias=True)\n  (fc2): Linear(in_features=120, out_features=84, bias=True)\n  (fc3): Linear(in_features=84, out_features=10, bias=True)\n)\n"
 }
]
```

```{.python .input  n=51}
def train(net, criterion, trainloader, use_cuda=False):
    cuda_run = None
    if use_cuda and  torch.cuda.is_available():        
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        cuda_run = True
        net = net.to(device)
#         criterion = criterion.to(device)
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

    for epoch in range(2):  # loop over the dataset multiple times
        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = data            
            if cuda_run:
                inputs = inputs.to(device)
                labels = labels.to(device)

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            if i % 2000 == 1999:    # print every 2000 mini-batches
                print('[%d, %5d] loss: %.3f' %
                      (epoch + 1, i + 1, running_loss / 2000))
                running_loss = 0.0
```

```{.python .input  n=52}
criterion = nn.CrossEntropyLoss()
```

```{.python .input  n=53}
net = Net()
with util.TaskTime('training', True):
    train(net, criterion, trainloader, use_cuda=True)   
```

```{.json .output n=53}
[
 {
  "name": "stderr",
  "output_type": "stream",
  "text": "2020-01-13 09:14:01,853: INFO: start training\n"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "[1,  2000] loss: 2.219\n[1,  4000] loss: 1.831\n[1,  6000] loss: 1.625\n[1,  8000] loss: 1.546\n[1, 10000] loss: 1.494\n[1, 12000] loss: 1.438\n[2,  2000] loss: 1.343\n[2,  4000] loss: 1.322\n[2,  6000] loss: 1.282\n[2,  8000] loss: 1.238\n[2, 10000] loss: 1.220\n[2, 12000] loss: 1.212\n"
 },
 {
  "name": "stderr",
  "output_type": "stream",
  "text": "2020-01-13 09:15:44,958: INFO: finish training [elapsed time: 103.11 seconds]\n"
 }
]
```

```{.python .input  n=45}
net = Net()
with util.TaskTime('training', True):
    train(net, criterion, trainloader, use_cuda=False)   
```

```{.json .output n=45}
[
 {
  "name": "stderr",
  "output_type": "stream",
  "text": "2020-01-13 09:08:19,044: INFO: start training\n"
 },
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "[1,  2000] loss: 2.161\n[1,  4000] loss: 1.816\n[1,  6000] loss: 1.639\n[1,  8000] loss: 1.560\n[1, 10000] loss: 1.489\n[1, 12000] loss: 1.445\n[2,  2000] loss: 1.360\n[2,  4000] loss: 1.346\n[2,  6000] loss: 1.293\n[2,  8000] loss: 1.285\n[2, 10000] loss: 1.265\n[2, 12000] loss: 1.238\n"
 },
 {
  "name": "stderr",
  "output_type": "stream",
  "text": "2020-01-13 09:10:48,281: INFO: finish training [elapsed time: 149.24 seconds]\n"
 }
]
```


