**通用**

~~~shell
top
glances        #pip install glances  硬件全面信息
~~~

**端口情况**

```shell
lsof -i:80  
netstat -lnp | grep 80
sudo iptables -t nat -L -n
```

## **其他**

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
cat /etc/*release*       #显示操作系统信息
cat /proc/uptime         #查看系统运行时间：。第一列 ：系统启动到现在的时间（秒），第二列：系统空闲的时间（秒）

cat /proc/version        #查看linux内核版本
cat /proc/cmdline        #查看系统启动参数：
~~~

**操作系统版本**

~~~shell
cat /etc/redhat-release  #centos
cat /proc/version        #查看内核
~~~

[*http://cdn.malu.me/cpu/*](http://cdn.malu.me/cpu/)                  *#天梯*

[*http://topic.expreview.com/CPU/*](http://topic.expreview.com/CPU/)     *#天梯*

![img](images/untitle.jpe)

### my laptop

电脑型号		惠普HP ZBook 15 G5笔记本
处理器			Intel(R) Core(TM) i7-8850H CPU @ 2.60GHz
内存容量			16.0GB
显卡			1、NVIDIA Quadro P1000
			        2、Intel(R) UHD Graphics 630
硬盘			SAMSUNG MZVLB512HAJQ-000H1 (512GB)
主板			842A (KBC Version 15.31.00)
网卡			1、Intel(R) Wireless-AC 9560
			        2、Intel(R) Ethernet Connection (7) I219-LM
声卡			1、High Definition Audio Device
			        2、Intel(R) Display Audio
显示器			CMN:f615  分辨率:1920x1080 
当前操作系统			Windows 10 64位

DIMM1	三星 DDR4 2666MHz 16GB
制造日期	2018 年 42 周
型号	CE M471A2K43DB1-CTD
序列号	411A03E5
	