---
title: 常用数据集
categories: others
date: 2020-10-22
---

本文主要介绍一些常用的数据集，并采用python代码来获取它们。不定期更新中。

## MNIST

![img](images/8389494-c279133be28eb263.webp)

[MNIST](http://yann.lecun.com/exdb/mnist/)（Mixed National Institute of Standards and Technology）数据集是著名的手写数字数据集，被誉为数据科学领域的`果蝇`。数据分为四部分。

| 数据文件                                                     | 描述         | 数据量 |
| ------------------------------------------------------------ | ------------ | ------ |
| [train-images-idx3-ubyte.gz](http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz) | training图片 | 60,000 |
| [train-labels-idx1-ubyte.gz](http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz) | training标签 | 60,000 |
| [t10k-images-idx3-ubyte.gz](http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz) | test图片     | 10,000 |
| [t10k-labels-idx1-ubyte.gz](http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz) | test标签     | 10,000 |

其中每张图片由$28 \times 28$ 个像素点构成，每个像素点用一个灰度值($0-255$)表示。

### 数据下载

~~~python
import gzip
import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import six.moves.urllib as urllib

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)

def mnist_download(target_path, source_url='http://yann.lecun.com/exdb/mnist', http_proxy=None):
    if http_proxy is not None:
        proxy_handler = urllib.request.ProxyHandler({'http': http_proxy, 'https': http_proxy})
        opener = urllib.request.build_opener(proxy_handler)
    else:
        opener = urllib.request.build_opener()

    urllib.request.install_opener(opener)

    def maybe_download(file_name):
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        file_path = os.path.join(target_path, file_name)
        if not os.path.exists(file_path):
            source_file_url = os.path.join(source_url, file_name)
            logging.info(source_file_url)
            filepath, _ = urllib.request.urlretrieve(source_file_url, file_path)
            statinfo = os.stat(filepath)
            logging.info('Successfully downloaded {} {} bytes.'.format(file_name, statinfo.st_size))
        return file_path

    train_data_path= maybe_download('train-images-idx3-ubyte.gz')
    train_label_path = maybe_download('train-labels-idx1-ubyte.gz')
    test_data_path= maybe_download('t10k-images-idx3-ubyte.gz')
    test_label_path = maybe_download('t10k-labels-idx1-ubyte.gz')
    return train_data_path, train_label_path, test_data_path, test_label_path

local_path = os.path.join('.', 'data/mnist')
train_data_path, train_label_path, test_data_path, test_label_path = mnist_download(local_path)
~~~

![image-20201021215101549](images/image-20201021215101549.png)

### 读取数据

下面抽取其中的label和data。

~~~python
def extract_label(file_path, num_images):
    """
    Extract the labels into a vector of label IDs.
    """

    logging.info('Extracting {}'.format(file_path))
    with gzip.open(file_path) as bytestream:
        bytestream.read(8)
        buf = bytestream.read(1 * num_images)
        labels = np.frombuffer(buf, dtype=np.uint8).astype(np.int64)
        return labels
    
def extract_data(file_path, num_images, normalize=False):
    """输出格式为3D Array[image index, height, width].

    对于同一MNIST, 其channel为1. 如果normalize为True，图片的灰度值从[0, 255]转换到[-0.5, 0.5].
        """
    image_size = 28
    pixel_depth = 255

    logging.info('Extracting {}'.format(file_path))
    with gzip.open(file_path) as bytestream:
        # Skip the magic number and dimensions; we know these values.
        bytestream.read(16)

        buf = bytestream.read(image_size * image_size * num_images)
        data = np.frombuffer(buf, dtype=np.uint8).astype(np.float32)
        if normalize: data = data/pixel_depth - 0.5
        data = data.reshape(num_images, image_size, image_size)
        return data
    

train_data = extract_data(train_data_path, 60000)
train_label = extract_label(train_label_path, 60000)
test_data = extract_data(test_data_path, 10000) 
test_label = extract_label(test_label_path, 10000)

print(train_data.shape)
print(train_label.shape)
print(test_data.shape)
print(test_label.shape)
~~~

![image-20201022110316545](images/image-20201022110316545.png)

显示其中的图片。

~~~python
plt.figure(figsize=(10,10))
for i in range(36):
    plt.subplot(6,6,i+1)
    plt.tight_layout()
    plt.imshow(train_data[i], cmap='gray', interpolation='none')
    plt.title("label: {}".format(train_label[i]))
    plt.xticks([])
    plt.yticks([])
~~~

![image-20201121164245572](images/image-20201121164245572.png)

## Fashion MNIST

![img](images/fashion-mnist-sprite.png)

[Fashion-MNIST](https://github.com/zalandoresearch/fashion-mnist)是一个替代MNIST手写数字集的图像数据集。 它是由Zalando（一家德国的时尚科技公司）旗下的研究部门提供，它其涵盖了来自10种类别的共7万个不同商品的正面图。Fashion-MNIST完全克隆了MNIST的所有外在特征。

- 60000张训练图像和对应Label

- 10000张测试图像和对应Label

- 10个类别

  | Label |    Description     |
  | :---: | :----------------: |
  |   0   | T恤（T-shirt/top） |
  |   1   |  裤子（Trouser）   |
  |   2   | 套头衫（Pullover） |
  |   3   |  连衣裙（Dress）   |
  |   4   |    外套（Coat）    |
  |   5   |   凉鞋（Sandal）   |
  |   6   |   衬衫（Shirt）    |
  |   7   | 运动鞋（Sneaker）  |
  |   8   |     包（Bag）      |
  |   9   | 靴子（Ankle boot） |

- 每张图像28x28的分辨率，每个像素点用一个灰度值($0-255$)表示

- 4个GZ文件名称都一样

  | 数据文件                                                     | 描述         | 数据量 |
  | ------------------------------------------------------------ | ------------ | ------ |
  | [train-images-idx3-ubyte.gz](http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz) | training图片 | 60,000 |
  | [train-labels-idx1-ubyte.gz](http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz) | training标签 | 60,000 |
  | [t10k-images-idx3-ubyte.gz](http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz) | training图片 | 10,000 |
  | [t10k-labels-idx1-ubyte.gz](http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz) | training标签 | 10,000 |

Fashion-MNIST出现的原因之一是，MNIST太简单了。虽然MNIST被誉为数据科学领域的`果蝇`，但目前很多算法都能在其测试集上取得99.6%的超高准确率。

### 数据下载

的确不愧是MNIST的替代，只要设置source_url到新的地址，就可以下载了。

~~~python
local_path = os.path.join('.', 'data/fashion-mnist')
train_data_path, train_label_path, test_data_path, test_label_path = mnist_download(local_path, source_url='http://fashion-mnist.s3-website.eu-central-1.amazonaws.com')
~~~

![image-20201028072757363](images/image-20201028072757363.png)

### 读取数据

同样可以调用上文MNIST中的方法。

~~~python
train_data = extract_data(train_data_path, 60000)
train_label = extract_label(train_label_path, 60000)
test_data = extract_data(test_data_path, 10000) 
test_label = extract_label(test_label_path, 10000)

print(train_data.shape)
print(train_label.shape)
print(test_data.shape)
print(test_label.shape)
~~~

![image-20201028083349086](images/image-20201028083349086.png)

显示其中的图片。

~~~python
labels = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal',
           'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

plt.figure(figsize=(10,10))
for i in range(36):
    plt.subplot(6,6,i+1)
    plt.tight_layout()
    plt.imshow(train_data[i], cmap='gray', interpolation='none')
    plt.title("label: {}".format(labels[train_label[i]]))
    plt.xticks([])
    plt.yticks([])
~~~

![image-20201121164430279](images/image-20201121164430279.png)

## CIFAR10

![cifar10](images/cifar10.png)

[CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html)数据集由10类32x32的RGB图片组成，一共包含60000张图片，每一类包含6000图片。其中50000张图片作为训练集，10000张图片作为测试集。

CIFAR-10数据集被划分成了5个训练的batch和1个测试的batch，每个batch均包含10000张图片。测试集batch的图片是从每个类别中随机挑选的1000张图片组成的,训练集batch以随机的顺序包含剩下的50000张图片。所有这些数据保存在一个压缩文件里，下载地址是：https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz。

### 数据下载

~~~python
import logging
import os
import pickle
import tarfile
import six.moves.urllib as urllib

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)

def cifar10_download_and_extract(target_path, source_url="https://www.cs.toronto.edu/~kriz", http_proxy=None):
    if http_proxy is not None:
        proxy_handler = urllib.request.ProxyHandler({'http': http_proxy, 'https': http_proxy})
        opener = urllib.request.build_opener(proxy_handler)
    else:
        opener = urllib.request.build_opener()

    urllib.request.install_opener(opener)

    def maybe_download(file_name):
        if not os.path.exists(target_path):
            os.mkdir(target_path)
        file_path = os.path.join(target_path, file_name)
        if not os.path.exists(file_path):
            source_file_url = os.path.join(source_url, file_name)
            logging.info(source_file_url)
            filepath, _ = urllib.request.urlretrieve(source_file_url, file_path)
            statinfo = os.stat(filepath)
            logging.info('Successfully downloaded {} {} bytes.'.format(file_name, statinfo.st_size))
        return file_path
    
    tar_gz_file = 'cifar-10-python.tar.gz'
    data_path= maybe_download(tar_gz_file)
    
    # extract the tar.gz file
    extract_path = os.path.join(target_path, "cifar-10-batches-py")
    logging.info("extract {} to {}".format(tar_gz_file, extract_path))
    with tarfile.open(data_path, 'r:gz') as tar:        
        tar.extractall(path=target_path)
    return extract_path

local_path = os.path.join('.', 'data/cifar10')
data_path = cifar10_download_and_extract(local_path)
~~~

![image-20201022133621391](images/image-20201022133621391.png)

下载并解压后，其目录结构如下。其中batch 1-5是5个训练数据集，而test_batch是测试数据集。

![image-20201022132953540](images/image-20201022132953540.png)

### 读取数据

~~~python
def extract_data_label(files):
    data = []
    label = []    
    for file in files:
        with open(file, 'rb') as fo:
            entry = pickle.load(fo, encoding='latin1')
        data.append(entry['data'])
        label.extend(entry['labels'])
 
    data = np.vstack(data)
    data = data.reshape(-1, 3, 32, 32)
    data = data.transpose((0, 2, 3, 1))   
    label = np.array(label)
    return data, label

train_files = ['data_batch_1', 'data_batch_2', 'data_batch_3', 'data_batch_4', 'data_batch_5']
train_files = [ os.path.join(data_path, file)  for file in train_files]
test_files = [ os.path.join(data_path, 'test_batch')]

train_data, train_label = extract_data_label(train_files)
test_data, test_label = extract_data_label(test_files)

print(train_data.shape)
print(train_label.shape)
print(test_data.shape)
print(test_label.shape)
~~~

![image-20201022141210090](images/image-20201022141210090.png)

显示其中的图片。

~~~python
plt.figure(figsize=(10,10))
classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

for i in range(36):
    plt.subplot(6,6,i+1)
    plt.tight_layout()
    plt.imshow(train_data[i])
    plt.title("label: {}".format(classes[train_label[i]]))
    plt.xticks([])
    plt.yticks([])
~~~

![image-20201121164935368](images/image-20201121164935368.png)



## IMDb : Large Movie Review Dataset

**IMDb**（Internet Movie Datebase ）是全球最大的互联网影视数据库，而[Large Movie Review Dataset](https://ai.stanford.edu/~amaas/data/sentiment/) 是一个根据IMDB上电影评论而建立的数据集。它由斯坦福大学于 2011 年发布，相关论文有[Learning Word Vectors for Sentiment Analysis](https://ai.stanford.edu/~ang/papers/acl11-WordVectorsSentimentAnalysis.pdf)。

Large Movie Review Dataset包括 50,000 条标记情感的电影评论，其中正面（positive）和负面（negative）的数量各半，然后这些数据又被均匀的分为训练数据和测试数据。此外，它还有 50,000 条未标记情感的评论。在数据集中，每个电影的评论数不超过30条。需要注意的是，每一条标记情感的评论是极端正面或极端负面的，不包括中立的评论。规则如下。

- $score \le 4$：负面评论
- $score \ge 7$：正面评论

数据集下载地址是https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz

### 数据下载

~~~python
import gzip
import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import tarfile
import six.moves.urllib as urllib

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)

def lmrd_download_and_extract(target_path, source_url='https://ai.stanford.edu/~amaas/data/sentiment/', http_proxy=None):
    if http_proxy is not None:
        proxy_handler = urllib.request.ProxyHandler({'http': http_proxy, 'https': http_proxy})
        opener = urllib.request.build_opener(proxy_handler)
    else:
        opener = urllib.request.build_opener()

    urllib.request.install_opener(opener)

    def maybe_download(file_name):
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        file_path = os.path.join(target_path, file_name)
        if not os.path.exists(file_path):
            source_file_url = os.path.join(source_url, file_name)
            logging.info(source_file_url)
            filepath, _ = urllib.request.urlretrieve(source_file_url, file_path)
            statinfo = os.stat(filepath)
            logging.info('Successfully downloaded {} {} bytes.'.format(file_name, statinfo.st_size))
        return file_path

    tar_gz_file = 'aclImdb_v1.tar.gz'
    data_path= maybe_download(tar_gz_file)
    
    # extract the tar.gz file
    extract_path = os.path.join(target_path, "aclImdb")
    logging.info("extract {} to {}".format(tar_gz_file, extract_path))
    with tarfile.open(data_path, 'r:gz') as tar:        
        tar.extractall(path=target_path)
    return extract_path

local_path = os.path.join('.', 'data/lmrd')
data_path = lmrd_download_and_extract(local_path)
~~~

![image-20201104120005508](images/image-20201104120005508.png)

下载并解压后，其目录结构如下。

![image-20201104115404253](images/image-20201104115404253.png)

- README：数据集说明。

- imdbEr.txt

  imdbEr.txt contains the expected rating for each token in imdb.vocab as computed by (Potts, 2011). The expected rating is a good way to get a sense for the average polarity of a word in the dataset.

  ~~~shell
  head imdbEr.txt
  ~~~

  ![image-20201104135810896](images/image-20201104135810896.png)

- imdb.vocab：总共有89,527个单词

  ~~~shell
  head imdb.vocab
  ~~~

  ![image-20201104135329191](images/image-20201104135329191.png)

- train：训练数据

  - labeledBow.feat：文件是[LIBSVM](https://blog.csdn.net/yangshaojun1992/article/details/87861767)数据格式。采用BOW方法对训练集25,000评论进行编码。下面是其中一行数据。

    ![image-20201104135041675](images/image-20201104135041675.png)

    其中`7`表示评分。`2:8`表示token为2的单词出现了7次。所有单词列表见imdb.vocab文件。

  - unsupBow.feat：文件是LIBSVM格式。采用BOW方法对未标记的50,000评论进行编码。

  - urls_neg.txt：原本这个文件里有每个评论的url地址，但由于IMDB网站的变化，无法指向具体的评论，所以只提供了所评论电影的链接。

  - urls_pos.txt：同上

  - urls_unsup.txt：同上

  - neg：该目录包含12,500个负面评论的文本文件。

    ~~~shell
    ll train/neg | head -10
    ~~~

    ![image-20201104124737226](images/image-20201104124737226.png)

    每个文件名都是[id]_[rating].txt的格式。

    - id：唯一编号
    - rating：表示用户的打分。从1-10。。可以看到rating都是大于等于4的。

  - pos：该目录包含12,500个正面评论的文本文件。

    ~~~shell
    ll train/pos | head -10
    ~~~

    ![image-20201104125223528](images/image-20201104125223528.png)
  
    每个文件名也都是[id]_[rating].txt的格式。可以看到rating都是大于等于7的。

  - unsup：该目录包含50,000个正面评论的文本文件。

    ~~~shell
    ll train/unsup | head -10
    ~~~

    ![image-20201104125513716](images/image-20201104125513716.png)

    每个文件名也都是[id]_[rating].txt的格式。只是所有的rating都是0。

- test：参考上面train目录下同名文件

### 读取数据

查看正面评论文件。

~~~python
train_dir = os.path.join(data_path, 'train/pos')
pos_files = os.listdir(train_dir)
for file_name in pos_files[0:3]:    
    file_path = os.path.join(train_dir, file_name)
    print('-'*30 + file_path + '-'*30 )
    with open(file_path) as f:
        comment = f.read() 
        print(comment if len(comment)<=800 else comment[0:800]+' ...')    
~~~

![image-20201105141514092](images/image-20201105141514092.png)

查看负面评论文件。

~~~python
train_dir = os.path.join(data_path, 'train/neg')
pos_files = os.listdir(train_dir)
for file_name in pos_files[0:3]:    
    file_path = os.path.join(train_dir, file_name)
    print('-'*30 + file_path + '-'*30 )
    with open(file_path) as f:
        comment = f.read() 
        print(comment if len(comment)<=800 else comment[0:800]+' ...')    
~~~

![image-20201105141742737](images/image-20201105141742737.png)

## EuroSAT dataset

![Image Name](images/q74ercqrjz.png)

[EuroSAT dataset](https://github.com/phelber/EuroSAT)是基于哨兵2号（Sentinel-2）卫星拍摄的图像收集而成，覆盖了13个光谱带，由10个分类组成，总共27,000张带标签和地理参考的土地使用图像。用于检测土地使用分类和土地覆盖变化等问题的研究，以帮助改善地理环境。数据集包含以下十类，每类包含2000～3000张图片，图片像素为64x64。

- Industrial Buildings 工业建筑
- Residential Buildings 居民楼
- Annual Crop 庄稼作物
- Permanent Crop 永久性作物
- River 河
- Sea & Lake 海洋湖泊
- Herbaceous Vegetation 草本植被
- Highway 高速公路
- Pasture 牧场
- Forest 森林

各类图片示例如下：

![Image Name](images/q74ermu6td.png)

数据集下载地址是http://madm.dfki.de/files/sentinel/EuroSAT.zip

### 数据下载

~~~python
import logging
import os
import matplotlib.pyplot as plt
import numpy as np
import zipfile
import six.moves.urllib as urllib
from PIL import Image

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)

def eurosat_download_and_extract(target_path, source_url="http://madm.dfki.de/files/sentinel", http_proxy=None):
    if http_proxy is not None:
        proxy_handler = urllib.request.ProxyHandler({'http': http_proxy, 'https': http_proxy})
        opener = urllib.request.build_opener(proxy_handler)
    else:
        opener = urllib.request.build_opener()

    urllib.request.install_opener(opener)

    def maybe_download(file_name):
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        file_path = os.path.join(target_path, file_name)
        if not os.path.exists(file_path):
            source_file_url = os.path.join(source_url, file_name)
            logging.info(source_file_url)
            filepath, _ = urllib.request.urlretrieve(source_file_url, file_path)
            statinfo = os.stat(filepath)
            logging.info('Successfully downloaded {} {} bytes.'.format(file_name, statinfo.st_size))
        return file_path
    
    tar_gz_file = 'EuroSAT.zip'
    data_path= maybe_download(tar_gz_file)
    
    # extract the tar.gz file
    extract_path = os.path.join(target_path, "2750")
    logging.info("extract {} to {}".format(tar_gz_file, extract_path))
    with zipfile.ZipFile(data_path, 'r') as zip_ref:
        zip_ref.extractall(target_path)
    return extract_path

local_path = os.path.join('.', 'data/eurosat')
data_path = eurosat_download_and_extract(local_path)
~~~

![image-20201119104546525](images/image-20201119104546525.png)

下载并解压后，其目录结构如下。

![image-20201119095811686](images/image-20201119095811686.png)

2750目录下有10个文件夹，对应上节说的10个类，每个文件夹下有2000~3000个文件。

![image-20201119100340018](images/image-20201119100340018.png)

### 读取数据

首先看看这些图片都是什么样子的。

~~~python
plt.figure(figsize=(13,13))

i = -1
label_cnt = 10
for label in os.listdir(data_path): 
    files = os.listdir(os.path.join(data_path, label))
    i = i+1
    if i>=label_cnt: break 
    for j in range(label_cnt):
        plt.subplot(label_cnt, label_cnt, label_cnt*i+j+1)
        plt.tight_layout()
        file_path =  os.path.join(data_path, label, files[j])
        image = Image.open(file_path)
        if j==0: plt.text(0, 10, label, color='red')
        plt.imshow(image)
        plt.xticks([])
        plt.yticks([])

plt.subplots_adjust(wspace=0, hspace=0)        
plt.show()
~~~

![image-20201119112945640](images/image-20201119112945640.png)

接下来是把这些图片转化到numpy的narrary中去。

~~~python
def extract_data_label(data_path, labels):
    data = []
    label = []    
    
    i = 0
    for child in labels: 
        files = os.listdir(os.path.join(data_path, child))
        for file in files:
            file_path =  os.path.join(data_path, child, file)
            image = Image.open(file_path)
            x = np.asarray(image)
            data.append(x)
            label.append(i)
        i = i + 1

    data = np.stack(data, axis=0)
    label = np.array(label)
    return data, label

labels = os.listdir(data_path)
data, label = extract_data_label(data_path, labels)

print(data.shape)
print(label.shape)
print(labels)
~~~

![image-20201119121352528](images/image-20201119121352528.png)

最后来验证一下，看看我们的转化是否正确。

~~~python
plt.figure(figsize=(10,10))

indexes = np.random.randint(len(data), size=25)
for i,index in enumerate(indexes):

    plt.subplot(5,5,i+1)
    plt.tight_layout()
    plt.imshow(data[index])
    plt.title("{}".format(classes[label[index]]))
    plt.xticks([])
    plt.yticks([])
       
plt.show()    
~~~

![image-20201119122501919](images/image-20201119122501919.png)

## SVHN

![image-20201119122501919](images/examples_new.png)      

[The Street View House Numbers (SVHN)](http://ufldl.stanford.edu/housenumbers/)是一个为训练目标检测算法而“真实”存在的一个图像数据集，它来自于谷歌街景中的房屋号码。SVHN中有两种数据格式。

- Format 1： 是原始未经处理的街景中的房屋号，每张图片包含多个数字，见上面图片。数据文件如下。

  | 文件                                                         | 描述                                 |
  | ------------------------------------------------------------ | ------------------------------------ |
  | [train.tar.gz](http://ufldl.stanford.edu/housenumbers/train.tar.gz) | train数据。内含33402张png文件        |
  | [test.tar.gz](http://ufldl.stanford.edu/housenumbers/test.tar.gz) | test数据。内含13068张png文件         |
  | [extra.tar.gz](http://ufldl.stanford.edu/housenumbers/extra.tar.gz) | extra train数据。内含202353张png文件 |

  总共包含248,823张图片。格式一的数据用于识别图片中有几个数字，这些数字位置在什么地方。

- Format 2：每张图片代表一个从0-9的数，见下面图片。

  ![image-20201119122501919](images/32x32eg.png)

  数据文件如下。

  | 文件                                                         | 描述                                            |
  | ------------------------------------------------------------ | ----------------------------------------------- |
  | [train_32x32.mat](http://ufldl.stanford.edu/housenumbers/train_32x32.mat) | matlab格式的train数据。内含73257张图片。        |
  | [test_32x32.mat](http://ufldl.stanford.edu/housenumbers/test_32x32.mat) | matlab格式的test数据。内含26032张图片。         |
  | [extra_32x32.mat](http://ufldl.stanford.edu/housenumbers/extra_32x32.mat) | matlab格式的extra train数据。内含531131张图片。 |

  总共包含6,30,420张32x32的RGB图片。格式二的数据相对比较简单，就是一个经典的多分类问题。

可以两种格式中，看到extra数据集的数据量比train数据集的数据大得多，毫无疑问，如果把extra数据集也加入训练，训练的效果会大大加强的。

### 数据下载

~~~python
import h5py
import logging
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import random
import scipy.io as scio
import tarfile
import six.moves.urllib as urllib
from PIL import Image
from pprint import pprint

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)

def svhn_download_and_extract(target_path, foramt='format2', source_url="http://ufldl.stanford.edu/housenumbers/", http_proxy=None):
    if http_proxy is not None:
        proxy_handler = urllib.request.ProxyHandler({'http': http_proxy, 'https': http_proxy})
        opener = urllib.request.build_opener(proxy_handler)
    else:
        opener = urllib.request.build_opener()

    urllib.request.install_opener(opener)

    def maybe_download(file_name):
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        file_path = os.path.join(target_path, file_name)
        if not os.path.exists(file_path):
            source_file_url = os.path.join(source_url, file_name)
            logging.info(source_file_url)
            filepath, _ = urllib.request.urlretrieve(source_file_url, file_path)
            statinfo = os.stat(filepath)
            logging.info('Successfully downloaded {} {} bytes.'.format(file_name, statinfo.st_size))
        return file_path

    def extract_targz(tar_gz_file, extract_path):
        extract_path = os.path.join(target_path, extract_path)
        if not os.path.exists(extract_path):
            logging.info("extract {} to {}".format(os.path.basename(tar_gz_file), extract_path))
            with tarfile.open(tar_gz_file, 'r:gz') as tar:        
                tar.extractall(path=target_path)
        return extract_path
            
    assert (foramt == 'format2' or foramt == 'format1')
    if foramt == 'format2':
        train_file = 'train_32x32.mat'
        test_file = 'test_32x32.mat'
        extra_file = 'extra_32x32.mat'
    else:
        train_file = 'train.tar.gz'
        test_file = 'test.tar.gz'
        extra_file = 'extra.tar.gz'        
        
    train_path= maybe_download(train_file)
    test_path= maybe_download(test_file)
    extra_path= maybe_download(extra_file)    
    
    # extract the tar.gz file
    if foramt == 'format1': 
        train_path = extract_targz(train_path, 'train')
        test_path = extract_targz(test_path, 'test')
        extra_path = extract_targz(extra_path, 'extra')
    return train_path, test_path, extra_path

f1_train_path, f1_test_path, f1_extra_path = svhn_download_and_extract('./data/svhn/format1', foramt='format1')
f2_train_path, f2_test_path, f2_extra_path = svhn_download_and_extract('./data/svhn/format2', foramt='format2')
~~~

![image-20201121163703396](images/image-20201121163703396.png)

上面的代码将会生成两个目录format1和format2。

![image-20201121162909194](images/image-20201121162909194.png)

在format1目录下，三个tar.gz文件被对应解压到了train，test，extra目录。三个目录详情如下。

- train

  - 图片文件：33402张png文件 

  - digitStruct.mat：边界框数据，详细内容见下一节。

  - see_bboxes.m：一个matlab程序示例，在图片上画出所识别数字的边界框。如下所示。

    ~~~matlab
    load digitStruct.mat
    for i = 1:length(digitStruct)
        im = imread([digitStruct(i).name]);
        for j = 1:length(digitStruct(i).bbox)
            [height, width] = size(im);
            aa = max(digitStruct(i).bbox(j).top+1,1);
            bb = min(digitStruct(i).bbox(j).top+digitStruct(i).bbox(j).height, height);
            cc = max(digitStruct(i).bbox(j).left+1,1);
            dd = min(digitStruct(i).bbox(j).left+digitStruct(i).bbox(j).width, width);
    
            imshow(im(aa:bb, cc:dd, :));
            fprintf('%d\n',digitStruct(i).bbox(j).label );
            pause;
        end
    ~~~

- test

  - 图片文件：13068张png文件 
  - digitStruct.mat：边界框数据，详细内容见下一节。
  - see_bboxes.m：一个matlab程序示例，在图片上画出所识别数字的边界框。

- extra：额外训练数据。

  - 图片文件：202353张png文件 
  - digitStruct.mat：边界框数据，详细内容见下一节。
  - see_bboxes.m：一个matlab程序示例，在图片上画出所识别数字的边界框。

### 读取数据

根据两种格式来分别读取。

#### Format 1

首先要从digitStruct.mat读取所需数据。

~~~python
def get_img_name(f, idx=0):
    names = f['digitStruct/name']
    img_name = ''.join(map(chr, f[names[idx][0]][()].flatten()))
    return(img_name)

def get_img_boxes(f, idx=0):
    """
    get the 'height', 'left', 'top', 'width', 'label' of bounding boxes of an image
    :param f: h5py.File
    :param idx: index of the image
    :return: dictionary
    """
    bboxs = f['digitStruct/bbox']

    bbox_prop = ['height', 'left', 'top', 'width', 'label']
    meta = { key : [] for key in bbox_prop}

    box = f[bboxs[idx][0]]
    for key in box.keys():
        if box[key].shape[0] == 1:
            meta[key].append(int(box[key][0][0]))
        else:
            for i in range(box[key].shape[0]):
                meta[key].append(int(f[box[key][i][0]][()].item()))

    return meta

def extract_digit_struct(data_path, n=1):   
    f = load_digit_struct(data_path)
    max = f['digitStruct/name'].shape[0]
    digit_structs = []
    for _ in range(n):
        idx = random.randint(0, max)
        digit_struct = get_img_boxes(f, idx)
        digit_struct['img_file'] = os.path.join(data_path, get_img_name(f, idx)) 
        digit_structs.append(digit_struct)
    return digit_structs  


def load_digit_struct(datapath):
    # 加载digitStruct.mat文件
    digit_file = os.path.join(f1_train_path, 'digitStruct.mat')   
    f = h5py.File(digit_file, 'r') 

    return f

f = load_digit_struct(f1_train_path)

print("f =", f)
print("f.keys() =", f.keys())
print("f['digitStruct'].keys() =", f['digitStruct'].keys())
~~~

![image-20201122135535144](images/image-20201122135535144.png)

需要注意的是，如果使用sio.loadmat来加载digitStruct.mat，会报"`NotImplementedError: Please use HDF reader for matlab v7.3 files`"，所以采用h5py.File来加载。下面进一步来看看里面还有什么。

~~~python
names = f['digitStruct/name']
bboxs = f['digitStruct/bbox']
print("f['digitStruct/name'] =", names)
print("f['digitStruct/bbox'] =", bboxs)

print("names[0] =", names[0])
print("bboxs[0] =", bboxs[0])

print('-'*50)
# 第一个图片。
box = f[bboxs[0][0]]
print("f[names[0][0]][()] =\n", f[names[0][0]][()])  # 文件名，每个字符都用ascii编码
print("f[bboxs[0][0]].keys() =", box.keys())

# 第一个图片的第一个选取框
print("f[box['height'][0][0]][()] =", f[box['height'][0][0]][()])
print("f[box['left'][0][0]][()] =", f[box['left'][0][0]][()])
print("f[box['top'][0][0]][()] =", f[box['top'][0][0]][()])
print("f[box['width'][0][0]][()] =", f[box['width'][0][0]][()])
print("f[box['label'][0][0]][()] =", f[box['label'][0][0]][()])
~~~

![image-20201122135631429](images/image-20201122135631429.png)

关于HDF5文件结构，可以参考[HDF5 使用介绍](https://blog.csdn.net/Mrhiuser/article/details/69603826)。接下来加载一些图片的边界框数据。

~~~python
# 加载一些图片
digit_structs = extract_digit_struct(f1_train_path, 16)
pprint(digit_structs[0])
~~~

![image-20201122135928377](images/image-20201122135928377.png)

然后显示图片，并在图片上画上边界框。

~~~python
plt.figure(figsize=(16,8))

for i, digit_struct in enumerate(digit_structs): 
    ax = plt.subplot(4, 4, i+1)
    image = Image.open(digit_struct['img_file'])
    plt.imshow(image)
    labels = ''.join([str(label if label!=10 else 0) for label in digit_struct['label']])
    text = '{}*{}\n{}'.format(image.size[0], image.size[1], labels)
    plt.text(0, image.size[1]/2, text, color='red')
    for j in range(len(digit_struct['label'])):
        top = max(digit_struct['top'][j],1);
        height = min(digit_struct['height'][j], image.size[1]-digit_struct['top'][j]);
        left = max(digit_struct['left'][j],1);
        width = min(digit_struct['width'][j], image.size[0]-digit_struct['left'][j]);       
        rect = plt.Rectangle((left,top), width, height, fill=False, edgecolor = 'blue', linewidth=1)
        ax.add_patch(rect)
    plt.xticks([])
    plt.yticks([])

plt.subplots_adjust(wspace=0, hspace=0)        
plt.show()
~~~

![image-20201122140010027](images/image-20201122140010027.png)

从上面的图形可以看出，图片的size是大小不一的，清晰程度也相差很大。

#### Format 2

然后看看Format2里面有什么。

~~~python
def extract_data_label(data_path):
    data = sio.loadmat(data_path)
    #print(data['__header__'], data['__version__'], data['__globals__'], sep="\t")
    X = data['X'].swapaxes(0, 3).swapaxes(2, 3).swapaxes(1, 2)
    y = data['y']
    return X, y


train_data, train_label = extract_data_label(f2_train_path)
test_data, test_label  = extract_data_label(f2_test_path)
extra_data, extra_label = extract_data_label(f2_extra_path)

print(train_data.shape, train_label.shape)
print(test_data.shape, test_label.shape)
print(extra_data.shape, extra_label.shape)
~~~

![image-20201121174324148](images/image-20201121174324148.png)

显示其中图片。

~~~python
plt.figure(figsize=(10,10))

for i in range(36):
    plt.subplot(6,6,i+1)
    plt.tight_layout()
    index = random.randint(0, len(train_data))
    plt.imshow(train_data[index])
    plt.title("label: {}".format(train_label[index,0]))
    plt.xticks([])
    plt.yticks([])
plt.show()
    
print(np.unique(train_label))    
~~~

![image-20201121214512095](images/image-20201121214512095.png)

根据上面结果，需要注意的是：

- 标签10对应的是数字0，而在MNIST数据集中，标签0对应的数字是0。
- 很多图片中出现了多个数字，但仅仅以位于中间的数字代表该图片所属数字。
- 很多数字非常模糊，就是人来判断也需要多看两眼才行，无疑这个数据集分类的难度比MNIST大得多。

## Cats vs. Dogs

![Woof Meow](images/woof_meow.jpg)

[Cats vs. Dogs（猫狗大战）](https://www.kaggle.com/c/dogs-vs-cats)是2013年Kaggle一道赛题，利用给定的数据集，用算法实现猫和狗的识别。 训练集有图片25000张，猫和狗的数量都是各半的。测试集中有图片12500张，没有标记。

### 数据下载

数据集下载地址是https://www.kaggle.com/c/dogs-vs-cats/data。由于必须登录网站才能下载，所以只能在浏览器手工下载下来。

![image-20201126092955568](images/image-20201126092955568.png)

点击上面`Download All`下载后，将会得到一个文件`dogs-vs-cats.zip`，解开后，会有三个文件。

~~~shell
unzip dogs-vs-cats.zip -d dogs-vs-cats
~~~

![image-20201126093458324](images/image-20201126093458324.png)

其中sampleSumission.然后分别解开train.zip和test1.zip。

~~~shell
cd dogs-vs-cats
unzip train.zip 
unzip test1.zip 
~~~

解开后，在train和test1分别有25,000，12,500个jpg图片。由于这是Kaggle的比赛，所以train中的图片已经标记为cat或者dog了，而test1中的图片没有标记，需要使用模型进行预测，然后把预测结果提交到Kaggle上，这样可以得到准确率。

~~~shell
ll train/dog* | head  ; ll train/cat* | head
~~~

![image-20201126100756853](images/image-20201126100756853.png)

~~~shell
ll test1 | head 
~~~

![image-20201126101056313](images/image-20201126101056313.png)

### 读取数据

首先来看看训练数据。

~~~python
import os
import random
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import ImageDataGenerator

label_cnt = 6

train_path = 'data/dogs-vs-cats/train'
train_files = os.listdir(train_path)
random.seed(1031)
sample_indexes = np.random.randint(0, len(train_files), size = label_cnt*label_cnt ) 

plt.figure(figsize=(12,12))

for i, index in enumerate(sample_indexes): 
    plt.subplot(label_cnt, label_cnt, i+1)
    plt.tight_layout()
    file_name = train_files[index]
    file_path =  os.path.join(train_path, file_name)
    image = Image.open(file_path)
    plt.text(0, image.size[1]/2, '{}\n{}'.format(file_name[0:3],image.size), color='red')
    plt.imshow(image)
    plt.xticks([])
    plt.yticks([])

plt.subplots_adjust(wspace=0, hspace=0)        
plt.show()
~~~

![image-20201126103739298](images/image-20201126103739298.png)

可以看到，图片的分辨率是不同的。最为搞笑的是，上图中第二行第二张图分明是爱因斯坦的图片好不好，不过看起来，他的样子还真的蛮像一只狗狗的。

下面来把图片加载到numpy中，由于图片大小不一，下面使用TensorFlow中的[tf.keras.preprocessing.image.ImageDataGenerator](https://juejin.cn/post/6844904024915853319)来进行处理，把图片统一裁剪拉伸到$128\times128$。首先

~~~python
filenames = os.listdir(train_path)
classes = []
for filename in filenames:
    label = filename.split('.')[0]
    if label == 'dog':
        classes.append('1')
    else:
        classes.append('0')

df_train = pd.DataFrame({
    'filename': filenames,
    'class': classes
})

df_train.tail()
~~~

![image-20201126120049542](images/image-20201126120049542.png)

然后创建ImageDataGenerator。

~~~python
train_datagen = ImageDataGenerator(
    rescale=1./255,
)

train_generator = train_datagen.flow_from_dataframe(
    df_train,
    train_path,
    x_col="filename",
    y_col="class",  
    class_mode='binary',
    target_size=(128, 128),
    batch_size=36
)
~~~

![image-20201126120126456](images/image-20201126120126456.png)

最后我们来查看一下图片，所有的图片现在都是$128\times128$的尺寸了。

~~~python
plt.figure(figsize=(12, 12))

images, classes = train_generator.next()
for i, image in enumerate(images):
    plt.subplot(6, 6, i+1)
    plt.imshow(image)
    plt.xticks([])
    plt.yticks([])    

plt.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)      
plt.show()
~~~

![image-20201126120222899](images/image-20201126120222899.png)



## 参考

- [Fashion-MNIST：替代MNIST手写数字集的图像数据集](https://zhuanlan.zhihu.com/p/28847070)
- [EuroSAT土地使用情况图像数据集](https://www.kesci.com/mw/dataset/5e6b3125dd480d002c21c46c)
- [25个深度学习相关公开数据集](https://zhuanlan.zhihu.com/p/35449783)
- [Access SVHN data in Python using h5py](https://www.vitaarca.net/post/tech/access_svhn_data_in_python/)
- [Keras 数据预处理 ImageDataGenerator](https://juejin.cn/post/6844904024915853319)
- [计算机视觉领域经典的开放数据集](https://www.lizenghai.com/archives/2339.html)

## 历史

- 2020-10-22：初始版本。包含MNIST和CIFAR10数据集合

- 2020-10-27：新增数据集Fashion MNIST

- 2020-11-04：增加数据集Large Movie Review Dataset

- 2020-11-19：增加数据集EuroSAT dataset

- 2020-11-22：增加数据集SVHN

- 2020-11-26:：增加数据集Cats vs. Dogs

  

