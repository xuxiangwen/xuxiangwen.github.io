### linux查看端口占用情况

~~~shell
lsof -i:80  
netstat -lnp|grep 80
~~~

### JupyterLab

~~~python
container_name=jl
docker stop $container_name
docker rm $container_name

docker run -it  -d  --gpus all \
--name $container_name \
-v /home/grid/eipi10:/tf/eipi10 \
-p 28888:8888 -p 27007:7007 -p 26006-26015:6006-6015  \
jupyter/scipy-notebook:17aba6048f44 \
jupyter-lab --notebook-dir=/tf --ip 0.0.0.0 --no-browser --allow-root --NotebookApp.token='xxw'
~~~

安装一些必备路那件

~~~python
docker exec -it jl bash
pip install --upgrade pip 
pip install --upgrade tensorflow-gpu==2.4.0
pip install --upgrade numpy scipy pandas 
pip install --upgrade scikit-image 
pip install --upgrade gensim  
pip install --upgrade jieba 
pip install --upgrade pyyaml
pip install --upgrade sklearn 
pip install --upgrade psycopg2-binary 
pip install --upgrade pymysql 
pip install --upgrade torch torchvision 
~~~

上诉安装完后，如果运行如下代码，将会长久等待.

~~~python
import tensorflow as tf
print(tf.__version__)
print(tf.config.list_physical_devices('GPU'))
~~~

### Tensorflow

**cpu+docker compose**

~~~shell
cd ~/eipi10/docker-study/tensorflow
docker stack deploy -c docker-compose.yml tensorflow
docker exec -it tensorflow_cpu.1.$(docker service ps tensorflow_cpu -q -f "desired-state=running") bash
jupyter notebook list
~~~

**cpu**

~~~shell
docker stop tf-py3 
docker rm tf-py3
docker run -it  -d --name tf-py3 -v /home/grid/eipi10:/tf/eipi10 -p 28888:8888 -p 27007:7007  tensorflow/tensorflow:latest-py3-jupyter   jupyter-notebook --notebook-dir=/tf --ip 0.0.0.0 --no-browser --allow-root --NotebookApp.token='xxw'
docker start tf-py3
docker exec -it ts-py3 bash
~~~

**gpu**

既然大多数情况，都会创建gpu的版本，干脆用最简单的名字tf吧。而且TensorFlow 2.1 是支持 Python 2 的最后一个 TF 版本，之后，只支持python3，所以docker tag中也不再需要py3了

~~~shell
container_name=tf1
ports="-p 28888:8888 -p 27007:7007 -p 26006-26015:6006-6015"
version=2.6.1-gpu-jupyter

docker stop $container_name
docker rm $container_name
docker run -it -d --gpus all --name $container_name -v /home/grid/eipi10:/tf/eipi10 $ports tensorflow/tensorflow:$version  jupyter-notebook --notebook-dir=/tf --ip 0.0.0.0 --no-browser --allow-root --NotebookApp.token='xxw'
docker logs $container_name

# 再次启动
docker start $container_name
docker exec -it $container_name bash
~~~



~~~shell
container_name=tf
ports="-p 18888:8888 -p 17007:7007 -p 16006-16015:6006-6015"
version=latest-gpu-jupyter

docker stop $container_name
docker rm $container_name
docker run -it -d --gpus all --name $container_name -v /home/grid/eipi10:/tf/eipi10 $ports tensorflow/tensorflow:$version  jupyter-notebook --notebook-dir=/tf --ip 0.0.0.0 --no-browser --allow-root --NotebookApp.token='xxw'
docker logs $container_name

# 再次启动
docker start $container_name
docker exec -it $container_name bash
~~~

安装一些软件和python package。

~~~shell
#http_proxy='http://web-proxy.rose.hp.com:8080' apt-get update 
#http_proxy='http://web-proxy.rose.hp.com:8080' apt install -y openssh-server
apt-get update 
apt install -y openssh-server
scp grid@15.15.175.163:/home/grid/.ssh/id_rs*  /root/.ssh/
ll 

# pip install如果有连接错误，可以加上参数 --proxy http://web-proxy.rose.hp.com:8080
pip install --upgrade pip 
pip install --upgrade numpy scipy pandas 
pip install --upgrade scikit-image 
pip install --upgrade gensim  
pip install --upgrade jieba 
pip install --upgrade pyyaml
pip install --upgrade sklearn 
pip install --upgrade psycopg2-binary 
pip install --upgrade pymysql 
pip install --upgrade seaborn
# pip install --upgrade awscli --user 
pip install --upgrade torch torchvision 
pip install --upgrade ipyparams
pip install --upgrade nltk
pip install --upgrade spacy[cuda112]
pip install --upgrade tensorflow_hub
pip install --upgrade transformers
pip install --upgrade xlrd==1.2.0  # excle operation
pip install --upgrade openpyxl
pip3 install --upgrade Office365-REST-Python-Client==2.3.1
pip3 install --upgrade Ipython
pip3 install --upgrade ipykernel
pip3 install --upgrade flask flask_restful flask_cors
pip3 install --upgrade dash

pip3 install pydot  
apt install -y  graphviz
#echo export PATH=\"\$PATH:/root/.local/bin\" >> /root/.bashrc
~~~

## RASA

~~~
docker run -v $(pwd):/app rasa/rasa:3.0.0-full init --no-prompt
~~~



### Ruby开发环境

~~~shell
docker run -it -d --name ruby-lab -v "$PWD":/usr/src/myapp -w /usr/src/myapp ruby:latest
docker exec -it ruby-lab bash

# checking
ruby -v
gem -v
gcc -v
g++ -v
make -v

~~~

### PostgreSQL

~~~shell
tag=10.6
docker run --name postgresql1 \
--mount type=bind,src=/home/grid/eipi10/docker-volume/postgresql/datadir,dst=/var/lib/postgresql/data \
-e POSTGRES_PASSWORD='grid'  \
-p 5432:5432 \
-d postgres:$tag

# -e POSTGRES_DB=eipi -e POSTGRES_USER=grid   
#初次安装后，默认生成一个名为postgres的数据库和一个名为postgres的数据库用户。这里需要注意的是，
#同时还生成了一个名为postgres的Linux系统用户。

docker logs postgresql1  #monitor the output from the container
docker logs postgresql1 2>&1 | grep GENERATED 

#启动container
docker start postgresql1 

#停止container
docker stop postgresql1 

#登录mysql服务器
docker exec -it postgresql1 bash
~~~

### MySQL

https://dev.mysql.com/doc/refman/5.7/en/docker-mysql-getting-started.html

~~~shell
tag=5.7
docker pull mysql/mysql-server:$tag
docker run --name=mysql1 \
--mount type=bind,src=/home/grid/eipi10/docker-volume/mysql/my.cnf,dst=/etc/my.cnf \
--mount type=bind,src=/home/grid/eipi10/docker-volume/mysql/datadir,dst=/var/lib/mysql \
--mount type=bind,src=/home/grid/eipi10/docker-volume/mysql/scripts/,dst=/docker-entrypoint-initdb.d/ \
-p 3306:3306 \
-d mysql/mysql-server:$tag

  #查看root的随机代码  
docker logs mysql1  #monitor the output from the container
docker logs mysql1 2>&1 | grep GENERATED 

#启动container
docker start mysql1

#停止container
docker stop mysql1
docker stop mysql1 ; docker  rm mysql1 ; sudo rm -rf  /home/grid/eipi10/docker-volume/mysql/datadir/*; ll -a  /home/grid/eipi10/docker-volume/mysql/datadir

#登录mysql服务器
docker exec -it mysql1 bash
~~~

### Elasticserach

**官方** 

https://www.elastic.co/guide/en/elasticsearch/reference/7.2/docker.html

~~~shell
docker run -d -it --name es-7.2.0  -v /home/grid/eipi10/elasticsearch/data:/usr/share/elasticsearch/data -p 19200:9200 -p 19300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.2.0

docker exec -it es-7.2.0 bash
docker start es-7.2.0
~~~

**自建ELK**

https://github.com/deviantony/docker-elk

~~~shell
cd ~/eipi10/docker-elk
docker stack deploy -c docker-compose.yml elk
~~~

### Nodejs

~~~shell
docker run -it --rm --name nodejs  -v "$PWD":/usr/src/app -w /usr/src/app node:8 node your-daemon-or-script.js
~~~

### Spark+Jupyter

~~~shell
docker run -it --name jpt-spark --rm -v /home/grid/eipi10:/eipi10  -p 8888:8888 jupyter/all-spark-notebook start-notebook.sh --notebook-dir=/eipi10
~~~

### 战斗民族nlp课程

~~~shell
docker run -it  --name coursera-aml-nlp --rm -v /home/grid/eipi10/python-book/arsenal/notebook/course/natural-language-processing:/root/coursera  -p 58888:8080 akashin/coursera-aml-nlp
docker exec -it coursera-aml-nlp bash
~~~

### Hadoop-Spark

~~~shell
cd /home/grid/eipi10/docker-hadoop/centos-base
docker rmi --force microsheen/centos-base:latest
docker build -t microsheen/centos-base:latest .

cd /home/grid/eipi10/docker-hadoop/hadoop-base
docker stop hadoop-base-1
docker rmi --force microsheen/hadoop-base:0.1
docker build -t microsheen/hadoop-base:0.1 .
docker run -u grid -it --env-file  cluster.env --name hadoop-base-1 --rm microsheen/hadoop-base:0.1
docker run -u grid -it --env-file  cluster.env -d -v /sys/fs/cgroup:/sys/fs/cgroup:ro --name hadoop-base-1 --rm microsheen/hadoop-base:0.1
docker exec -it hadoop-base-1 bash
cat hadoop/etc/hadoop/core-site.xml

docker stack deploy -c docker-compose.yml hadoop
~~~

https://blog.newnius.com/setup-hadoop-cluster-based-on-docker-swarm.html   基于Docker Swarm搭建Hadoop集群

https://hacpai.com/article/1508232710946  基于 docker 搭建 hadoop 跨主机集群

### My Service

**file-server**

https://itbilu.com/nodejs/core/Nkvh9yS4W.html 文件下载服务器

**Hadoop-Spark**

*cd /home/grid/eipi10/docker-hadoop/centos-base*

*docker rmi --force microsheen/centos-base:latest*

*docker build -t microsheen/centos-base:latest .*

*cd /home/grid/eipi10/docker-hadoop/hadoop-base*

*docker stop hadoop-base-1*

*docker rmi --force microsheen/hadoop-base:0.1*

*docker build -t microsheen/hadoop-base:0.1 .*

*docker run -u grid -it* *--env-file  cluster.env* *--name hadoop-base-1 --rm microsheen/hadoop-base:0.1*

*docker run -u grid -it* *--env-file  cluster.env* *-d* *-v /sys/fs/cgroup:/sys/fs/cgroup:ro* *--name hadoop-base-1 --rm microsheen/hadoop-base:0.1*

*docker exec -it hadoop-base-1 bash*

*cat hadoop/etc/hadoop/core-site.xml*

*docker stack deploy -c docker-compose.yml hadoop*

https://blog.newnius.com/setup-hadoop-cluster-based-on-docker-swarm.html   基于Docker Swarm搭建Hadoop集群

https://hacpai.com/article/1508232710946  基于 docker 搭建 hadoop 跨主机集群

**Service**

**file-server**

https://itbilu.com/nodejs/core/Nkvh9yS4W.html 文件下载服务器

  

![image-20200618111522735](images/image-20200618111522735.png)

