### linux查看端口占用情况

~~~shell
lsof -i:80  
netstat -lnp|grep 80
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

~~~shell
docker run  -it --name es-7.1.1 --rm  -v /home/grid/eipi10/elasticsearch/data:/usr/share/elasticsearch/data -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.1.1
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
docker run -it  --name ts-py3 -v /home/grid/eipi10:/notebooks/eipi10 -p 28888:8888 -p 17007:7007  tensorflow/tensorflow:latest-py3  /run_jupyter.sh --allow-root --NotebookApp.token='xxw'
docker start ts-py3
docker exec -it ts-py3 bash
~~~

**gpu**

由于最新的image要求cuda>=10.0 ，所以并没有使用最新的image，只能用上一版本。

~~~shell
docker run -it  --runtime=nvidia --name ts-gpu-py3 -v /home/grid/eipi10:/notebooks/eipi10 -p 18888:8888 -p 17007:7007  tensorflow/tensorflow:1.12.0-gpu-py3   /run_jupyter.sh --allow-root --NotebookApp.token='xxw'
docker start ts-gpu-py3
docker exec -it ts-gpu-py3 bash
~~~

**tensorflow 1.5**

当时阿里nlp比赛时，使用了1.5

~~~shell
nvidia-docker run -it  --name ts-gpu-py2  -v /home/grid/eipi10:/notebooks/eipi10 -p 48888:8888 -p 37007:7007  tensorflow/tensorflow:1.5.0-gpu /run_jupyter.sh --allow-root --NotebookApp.token='xxw'
docker exec -it ts-gpu-py2 bash
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



  