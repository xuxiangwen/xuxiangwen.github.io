**通用**

~~~shell
top

glances        #pip install glances  硬件全面信息
~~~

**CPU**

~~~shell
cat /proc/cpuinfo                                        #CPU状态
watch -n 10 "cat /proc/cpuinfo |grep MHz|uniq"           #查看 cpu 内核频率
sudo sh -c "yes|sensors-detect"                          #检查sensors：  sudo yum install -y lm_sensors      
sensors                                                  #查看cpu温度
~~~

**内存**

~~~shell
cat /proc/meminfo                   #查看内存
sudo dmidecode -t memory            #内存内核频率
~~~

**Nvidia显卡**

~~~shell
watch -n 10 nvidia-smi   #Nvidia GPU状态, 每隔5秒监控 
nvidia-smi -a            #Nvidia GPU详细信息
gpustat                  #是一个输出格式比较简单的查看nvidia工具，通过pip install gpustat  --proxy http://web-proxy.rose.hp.com:8080，安装
~~~

**Linux系统**

~~~shell
cat /proc/uptime         #查看系统运行时间：。第一列 ：系统启动到现在的时间（秒），第二列：系统空闲的时间（秒）

cat /proc/version        #查看linux内核版本
cat /proc/cmdline        #查看系统启动参数：
~~~

**操作系统版本**

~~~shell
cat /etc/redhat-release  #centos
cat /proc/version        #查看内核
~~~

**端口情况**

~~~shell
lsof -i:80  
netstat -lnp|grep 80
~~~

**其他**

[*http://cdn.malu.me/cpu/*](http://cdn.malu.me/cpu/)                  *#天梯*

[*http://topic.expreview.com/CPU/*](http://topic.expreview.com/CPU/)     *#天梯*



![img](image/untitle.jpe)