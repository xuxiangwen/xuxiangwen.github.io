
## 1.1 安装

**history**

- 【2018-09-25】

```shell
## 环境
# 安装pip on ubuntu
http_proxy='http://web-proxy.rose.hp.com:8080' apt-get install -y  python3-pip

# 安装fontconfig on ubuntu
http_proxy='http://web-proxy.rose.hp.com:8080' apt-get install -y fontconfig

# update pip    
!pip install --upgrade pip --proxy http://web-proxy.rose.hp.com:8080   

### Python3   Port :18888
#### nlp
!pip install nltk --proxy http://web-proxy.rose.hp.com:8080  

#### PyTorch 
!pip install torch torchvision --proxy http://web-proxy.rose.hp.com:8080        
!pip install --upgrade gensim --proxy http://web-proxy.rose.hp.com:8080     
!pip install --upgrade scikit-image --proxy http://web-proxy.rose.hp.com:8080     
        
#以后安装方式，还是要参考官方文档

!pip install --upgrade pyyaml --proxy http://web-proxy.rose.hp.com:8080     

#### python 可视化
!pip install --upgrade seaborn --proxy http://web-proxy.rose.hp.com:8080  
!pip install --upgrade plotly --proxy http://web-proxy.rose.hp.com:8080 

#### rasa
!pip install --upgrade incremental --proxy http://web-proxy.rose.hp.com:8080   
!pip install --upgrade twisted --proxy http://web-proxy.rose.hp.com:8080    
!pip install -U rasa_nlu --proxy http://web-proxy.rose.hp.com:8080  
!pip install -U rasa_core --proxy http://web-proxy.rose.hp.com:8080  

#### mysql: read data from database
!pip install -U pymysql --proxy http://web-proxy.rose.hp.com:8080      

#### mysql: write data to database
!http_proxy='http://web-proxy.rose.hp.com:8080 ' apt install -y libmysqlclient-dev  # for ubuntu
#!pip install -U mysqlclient --proxy http://web-proxy.rose.hp.com:8080   
!pip install -U sqlalchemy --proxy http://web-proxy.rose.hp.com:8080 
!pip install -U mysql-connector --proxy http://web-proxy.rose.hp.com:8080 

#### redshift : read data from database
!pip install -U psycopg2-binary --proxy http://web-proxy.rose.hp.com:8080 

#### ssh:
!http_proxy='http://web-proxy.rose.hp.com:8080' apt-get update
!http_proxy='http://web-proxy.rose.hp.com:8080' apt install -y  openssh-server

#### gensim
!pip install --upgrade gensim --proxy http://web-proxy.rose.hp.com:8080 
#  Without Cython, youâll only be able to use one core because of the GIL (and word2vec training will be miserably slow).
!pip install --upgrade  Cython --install-option="--no-cython-compile"   --proxy http://web-proxy.rose.hp.com:8080    

#### nlp
!pip install --upgrade jieba --proxy http://web-proxy.rose.hp.com:8080  
!pip install --upgrade wordcloud --proxy http://web-proxy.rose.hp.com:8080  
!pip install --upgrade snownlp --proxy http://web-proxy.rose.hp.com:8080 
!pip install --upgrade pkuseg --proxy http://web-proxy.rose.hp.com:8080 
!pip install --upgrade thulac --proxy http://web-proxy.rose.hp.com:8080 

###  Python2   Port :48888
#### Ali NLP 比赛
!pip install --upgrade jieba==0.39 --proxy http://web-proxy.rose.hp.com:8080  
!pip install --upgrade keras==2.1.6 --proxy http://web-proxy.rose.hp.com:8080  
!pip install --upgrade sklearn==0.19.1 --proxy http://web-proxy.rose.hp.com:8080   
!pip install --upgrade gensim==3.4.0 --proxy http://web-proxy.rose.hp.com:8080  
!pip install --upgrade pytorch==0.4.0 --proxy http://web-proxy.rose.hp.com:8080  

### 安装aws  client
!pip install --upgrade awscli --user --proxy http://web-proxy.rose.hp.com:8080 
# 注意在 ts-gpu-py3 中，执行以下语句把aws路径添加到启动文件中。
# echo export PATH=\"\$PATH:/root/.local/bin\" >> /root/.bashrc

### Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python
!pip install -U  boto3 --proxy http://web-proxy.rose.hp.com:8080 

### 
!pip install -U  pyLDAvis --proxy http://web-proxy.rose.hp.com:8080 

!pip install -U  yaml --proxy http://web-proxy.rose.hp.com:8080 
```

```python
!pip install --upgrade wordcloud --proxy http://web-proxy.rose.hp.com:8080
```

```python
import tensorflow as tf
import pandas as pd
import numpy as np
import sklearn 
import keras
import torch
import nltk
import gensim

print('tf.__version__', tf.__version__)
print('keras.__version__', keras.__version__)
print('pd.__version__', pd.__version__)
print('np.__version__', np.__version__)
print('sklearn.__version__', sklearn.__version__)
print('torch.__version__', torch.__version__)
print('nltk.__version__', nltk.__version__)
print('gensim.__version__', gensim.__version__)

```

## 1.2  git忽略设置（.gitignore）

**history**

- 【2018-09-25】

```shell
cat >  .gitignore << EOF     #linux多行输出到文本
.ipynb_checkpoints
.idea
.env/*cd
*.pyc
*.swp
data
model
EOF

chmod 664 .gitignore
cat  .gitignore
```

## 1.3  notebook通用开始代码 

**history**

- 【2020-01-13】调整目录到
- 【2018-10-10】增加keras gpu内存限制
- 【2018-09-25】创建
~~~python
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

~~~

keras限定gpu的占用内存

```python
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.3
set_session(tf.Session(config=config))
```

## 1.4 ubuntu apt代理设置

代理设置，并安装软件。

~~~shell
echo Acquire::http::Proxy \"http://web-proxy.rose.hp.com:8080\"\; > /etc/apt/apt.conf.d/proxy.conf
echo Acquire::https::Proxy \"http://web-proxy.rose.hp.com:8080\"\; >> /etc/apt/apt.conf.d/proxy.conf
cat /etc/apt/apt.conf.d/proxy.conf
apt update
apt-get install -y openssh-server
~~~

## 1.5 CentOS升级

~~~
sudo yum clean all
sudo yum update -y
~~~



    - **1** (1-bit pixels, black and white, stored with one pixel per byte)
    - **L** (8-bit pixels, black and white)
    - **P** (8-bit pixels, mapped to any other mode using a colour palette)
    - **RGB** (3x8-bit pixels, true colour)
    - **RGBA** (4x8-bit pixels, true colour with transparency mask)
    - **CMYK** (4x8-bit pixels, colour separation)
    - **YCbCr** (3x8-bit pixels, colour video format)
    - **I** (32-bit signed integer pixels)
    - **F** (32-bit floating point pixels)

### update_file.sh

更新一些系统配置文件。当前目录的bin目录下，创建下面的文件

~~~shell
vi bin/update_file.sh

# !/bin/bash
script=$(readlink -f "$0")
script_path=$(dirname "$script")

filepath=$1
filename=`basename $filepath`
content=$2
append=${3:-append}

if [ ! -f "$filepath" ]; then
  echo $filepath can\'t be found
  exit
fi

owner_group=`stat --format '%U:%G' $filepath`
mode==`stat --format '%a' $filepath`

echo -----------------------------------------
echo tail -20  $filepath 
tail -20  $filepath 

echo -----------------------------------------
echo ls -l $filepath
ls -l $filepath

echo -----------------------------------------
while true; do
    read -p "Do you want to change $filepath[y/n]?" yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer y or n.";;
    esac
done

echo -----------------------------------------
if [ "$append" = "new" ];then
  echo create a new file: $filename
  touch $filename
else
  echo copy $filepath to $filename
  cp  $filepath $filename
fi 

echo change content in $filename
cat << EOF >> $filename
$2
EOF

echo -----------------------------------------
backup_file=$filepath.`date +%Y-%m-%d_%H-%M-%S`
echo backup $filepath to $backup_file
sudo cp $filepath $backup_file

echo move $filename to $filepath
sudo mv $filename $filepath
sudo chown $owner_group $filepath
sudo chmod $mode $filepath

echo -----------------------------------------
echo tail -20  $filepath 
tail -20  $filepath 

echo -----------------------------------------
echo ls -l $filepath $backup_file
ls -l $filepath $backup_file

~~~

设置文件链接

~~~shell
ln -s ~/eipi10/xuxiangwen.github.io/_notes/00-env/bin/update_file.sh ~/eipi10/bin/update_file.sh
~~~

测试

~~~shell
~/eipi10/bin/update_file.sh /etc/hosts \
"
15.38.197.155 aa02
15.38.197.239 aa03
"
~~~

