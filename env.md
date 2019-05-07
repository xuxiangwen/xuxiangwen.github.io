
## 1.1 安装

**history**

- 【2018-09-25】

```shell
## 环境
# 安装pip on ubuntu
http_proxy='http://web-proxy.rose.hp.com:8080 ' apt-get install -y  python3-pip

# 安装fontconfig on ubuntu
http_proxy='http://web-proxy.rose.hp.com:8080 ' apt-get install -y fontconfig

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


#### gensim
!pip install --upgrade gensim --proxy http://web-proxy.rose.hp.com:8080 
#  Without Cython, you’ll only be able to use one core because of the GIL (and word2vec training will be miserably slow).
!pip install --upgrade  Cython --install-option="--no-cython-compile"   --proxy http://web-proxy.rose.hp.com:8080    

#### nlp
!pip install --upgrade jieba --proxy http://web-proxy.rose.hp.com:8080  
!pip install --upgrade wordcloud --proxy http://web-proxy.rose.hp.com:8080  

###  Python2   Port :48888
#### Ali NLP 比赛
!pip install --upgrade jieba==0.39 --proxy http://web-proxy.rose.hp.com:8080  
!pip install --upgrade keras==2.1.6 --proxy http://web-proxy.rose.hp.com:8080  
!pip install --upgrade sklearn==0.19.1 --proxy http://web-proxy.rose.hp.com:8080   
!pip install --upgrade gensim==3.4.0 --proxy http://web-proxy.rose.hp.com:8080  
!pip install --upgrade pytorch==0.4.0 --proxy http://web-proxy.rose.hp.com:8080  

### 安装aws client
!pip install --upgrade awscli --user --proxy http://web-proxy.rose.hp.com:8080 

```


```python
!pip install --upgrade wordcloud --proxy http://web-proxy.rose.hp.com:8080
```

    Collecting wordcloud
    [?25l  Downloading https://files.pythonhosted.org/packages/5e/b7/c16286efa3d442d6983b3842f982502c00306c1a4c719c41fb00d6017c77/wordcloud-1.5.0-cp35-cp35m-manylinux1_x86_64.whl (357kB)
    [K    100% |################################| 358kB 535kB/s ta 0:00:01
    [?25hRequirement already satisfied, skipping upgrade: numpy>=1.6.1 in /usr/local/lib/python3.5/dist-packages (from wordcloud) (1.15.4)
    Requirement already satisfied, skipping upgrade: pillow in /usr/local/lib/python3.5/dist-packages (from wordcloud) (5.3.0)
    Installing collected packages: wordcloud
    Successfully installed wordcloud-1.5.0
    [33mYou are using pip version 18.1, however version 19.0.2 is available.
    You should consider upgrading via the 'pip install --upgrade pip' command.[0m



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

    Using TensorFlow backend.



    ---------------------------------------------------------------------------

    ImportError                               Traceback (most recent call last)

    <ipython-input-11-3220e153c764> in <module>
          4 import sklearn
          5 import keras
    ----> 6 import torch
          7 import nltk
          8 import gensim


    ImportError: No module named 'torch'


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

- 【2018-09-25】
- 【2018-10-10】增加keras gpu内存限制
**first**
```python
import sys
import logging


base_path = '/notebooks/eipi10/python-book/arsenal'
sys.path.append(base_path)
current_path = '.'
current_data_path = current_path + "/data"
current_model_path = current_path + "/model"


logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)

import collections
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import time


from pprint import pprint
from eipi10.ml2.utils import *

pd.set_option('display.width', 1000)
os.environ["https_proxy"] = "http://web-proxy.rose.hp.com:8080"
os.environ["http_proxy"] = "http://web-proxy.rose.hp.com:8080"

%matplotlib inline

# 代码自动重新加载
%load_ext autoreload
%autoreload 2

#当module有新的方法的时候，需要运行下面方法。
# %reload_ext autoreload 
```
keras限定gpu的占用内存
```python
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.3
set_session(tf.Session(config=config))
```
