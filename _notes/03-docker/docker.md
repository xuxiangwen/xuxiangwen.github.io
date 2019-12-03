## 1. 常见命令和资源

####  docker 在线书

 https://yeasy.gitbooks.io/docker_practice/content/

https://joshhu.gitbooks.io/dockercommands/content/

### 安装Docker

https://yeasy.gitbooks.io/docker_practice/content/install/centos.html

~~~shell
# 卸载旧版
sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-selinux \
                  docker-engine-selinux \
                  docker-engine
# 安装依赖包
sudo yum install -y yum-utils \
           device-mapper-persistent-data \
           lvm2

# 更新 yum 软件源缓存，并安装 docker-ce
sudo yum makecache fast
sudo yum install docker-ce

# 建立 docker 用户组
sudo groupadd docker
sudo usermod -aG docker $USER

# 测试Docker是否安装成功
docker run hello-world
~~~

### 启动docker

~~~shell
sudo systemctl enable docker
sudo systemctl start docker
~~~

### 创建 Swarm 集群

#### 初始化集群

~~~
docker swarm init
~~~

#### 加入swarm

~~~
docker swarm join --token SWMTKN-1-1ngrjkqk2356wfhuibeforvbfsn7rlfbol5foglcnegvsbcnd1-9aw3kcsq5ish8c0cs37cbpj8o 15.15.165.218:2377
~~~

