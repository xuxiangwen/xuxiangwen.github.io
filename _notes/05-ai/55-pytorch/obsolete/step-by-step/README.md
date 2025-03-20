# 前言

- 书

   [Deep Learning with PyTorch Step-by-Step A Beginner’s Guide.pdf](..\..\..\..\..\ai\book\machine_learning\Daniel Voigt Godoy - Deep Learning with PyTorch Step-by-Step A Beginner’s Guide (2022, leanpub.com) - libgen.li.pdf) 

- 代码

  https://github.com/dvgodoy/PyTorchStepByStep

## 环境

本书可以在多个环境中进行学习。

### Google Colab

-  https://colab.research.google.com/github/

### Binder

一个在线版的 Jupyter Notebook，用法很简洁，直接连接到 GitHub 储存库就可以像在本地一样使用 Jupyter Notebook 进行开发。

https://mybinder.org/v2/gh/dvgodoy/PyTorchStepByStep/master

### 本地安装

#### 下载代码库

~~~shell
 git clone https://github.com/dvgodoy/PyTorchStepByStep.git
~~~

#### 安装依赖包

- tensorboard 

  ~~~shell
  pip3 install tensorboard 
  ~~~

- 安装 graphviz

  [graphviz](https://graphviz.org/)是一个开源的图可视化工具。详细的安装步骤参见 [How to install Graphviz software](https://bobswift.atlassian.net/wiki/spaces/GVIZ/pages/20971549/How+to+install+Graphviz+software)。

  - fedora

    ~~~shell
    sudo yum install graphviz
    ~~~

    > Red Hat 有许多的 Linux 发行版，比如：CentOS、Fedora、RHEL以及 Fedora CoreOS等。Fedora是一个基于社区的免费发行版，专注于快速发布新功能。Fedora 是新技术/功能的试验场，它的一些功能也会被其它发布版所采用。Fedora是由 Red Hat 提供支持，对于企业需要的稳定和有用的所有内容，都可以逐步移交给 RHEL 发行版。

  - ubuntu

    ~~~shell
    sudo apt install graphviz
    ~~~

- 安装 torchviz

  torchviz用于创建PyTorch execution graphs and traces。其调用了graphviz。

  测试安装。

  ~~~python
  import torch
  from torchviz import make_dot
  v = torch.tensor(1.0, requires_grad=True)
  make_dot(v)
  ~~~

  ![image-20230409223550972](images/image-20230409223550972.png)

  如果graphviz和torchviz安装正确，将会显示上面这样的图形。否则报错。

# Chapter 0

实现

