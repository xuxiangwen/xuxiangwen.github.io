在Python开发中时，可能会有以下情况。

- 系统默认的Python版本和开发所需要的版本不同
- 开发多个应用程序, 可能会用到好几个版本的python环境

上述情况发生时，我们一定希望，每个应用各自拥有一套"独立"的Python运行环境，而virtualenv就是用来为一个应用创建一套"隔离"的Python运行环境的工具。virtualenv是python的一个虚拟化环境工具，用来建立一个虚拟的python环境，一个专属于项目的python环境。

### Install virtualenv

对于python2需要如下安装，而python3中绑定了venv模块，可以调用它来创建虚拟环境。

~~~shell
pip install virtualenv
~~~

### 创建目录

~~~shell
 mkdir virtualenv-test
 cd virtualenv-test
~~~

### 创建一个独立的Python运行环境

#### python2

~~~
 virtualenv venv 
~~~

或者

~~~shell
 virtualenv -p /home/grid/eipi10/aa/Python-3.6.10 venv
~~~

> 指定python版本的位置

命令`virtualenv`就可以创建一个独立的Python运行环境。

新建的Python环境被放到当前目录下的`venv`目录。有了`venv`这个Python环境，可以用`source`进入该环境：

~~~
source venv/bin/activate
~~~

#### python3

~~~shell
python3 -m venv venv
source venv/bin/activate
~~~

### 安装第三方包

~~~
pip install jinja2
~~~

### 退出当前的`venv`环境

~~~
deactivate 
~~~

## 参考

- [virtualenv](https://www.liaoxuefeng.com/wiki/1016959663602400/1019273143120480)

