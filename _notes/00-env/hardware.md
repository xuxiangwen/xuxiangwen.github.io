

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

#### 2022-06-01

|     **Motherboard:**            |                                  |                                                              |
| ---------------- | -------------------------------- | ------------------------------------------------------------ |
|                  | CPU Type                         | [OctalCore Intel Core i7-11800H, 4200 MHz (42 x 100)](https://ark.intel.com/content/www/us/en/ark/search.html?q=Intel Core i7-11800H) |
|                  | Motherboard Name                 | HP ZBook Fury 15.6 inch G8 Mobile Workstation PC             |
|                  | Motherboard Chipset              | [Intel Tiger Point WM590, Intel Tiger Lake-H](https://www.intel.com/products/chipsets) |
|                  | System Memory                    | [ TRIAL VERSION ]                                            |
|                  | DIMM1: SK hynix HMAA2GS6CJR8N-XN | 16 GB DDR4-3200 DDR4 SDRAM  (24-22-22-52 @ 1600 MHz)  (22-22-22-52 @ 1600 MHz)  (21-21-21-49 @ 1527 MHz)  (20-20-20-47 @ 1454 MHz)  (19-19-19-45 @ 1381 MHz)  (18-18-18-42 @ 1309 MHz)  (17-17-17-40 @ 1236 MHz)  (16-16-16-38 @ 1163 MHz)  (15-15-15-35 @ 1090 MHz)  (14-14-14-33 @ 1018 MHz)  (13-13-13-31 @ 945 MHz)  (12-12-12-28 @ 872 MHz)  (11-11-11-26 @ 800 MHz)  (10-10-10-24 @ 727 MHz) |
|                  | BIOS Type                        | Unknown (07/18/2022)                                         |

| **Display:** |                |                                                              |
| ------------ | -------------- | ------------------------------------------------------------ |
|              | Video Adapter  | [Intel(R) UHD Graphics  (1 GB)](https://www.intel.com/products/chipsets) |
|              | Video Adapter  | [Intel(R) UHD Graphics  (1 GB)](https://www.intel.com/products/chipsets) |
|              | Video Adapter  | [Intel(R) UHD Graphics  (1 GB)](https://www.intel.com/products/chipsets) |
|              | Video Adapter  | [Intel(R) UHD Graphics  (1 GB)](https://www.intel.com/products/chipsets) |
|              | Video Adapter  | [NVIDIA T1200 Laptop GPU  (4 GB)](https://www.nvidia.com/geforce) |
|              | Video Adapter  | [NVIDIA T1200 Laptop GPU  (4 GB)](https://www.nvidia.com/geforce) |
|              | Video Adapter  | [NVIDIA T1200 Laptop GPU  (4 GB)](https://www.nvidia.com/geforce) |
|              | Video Adapter  | [NVIDIA T1200 Laptop GPU  (4 GB)](https://www.nvidia.com/geforce) |
|              | 3D Accelerator | [nVIDIA T1200 Laptop](https://www.nvidia.com/geforce)        |
|              | Monitor        | Generic PnP Monitor [NoDB]                                   |
|              | Monitor        | [HP EliteDisplay E243 (HDMI)  [23.8" IPS LCD\]  (CNK90618L4)](http://www8.hp.com/us/en/products/monitors) |

| **Multimedia:** |               |                                                              |
| --------------- | ------------- | ------------------------------------------------------------ |
|                 | Audio Adapter | [Intel Tiger Point PCH - cAVS (Audio, Voice, Speech)](https://www.intel.com/products/chipsets) |
|                 | Audio Adapter | [nVIDIA TU117 HDMI/DP @ nVIDIA TU117 - High Definition Audio Controller](https://www.nvidia.com/page/mobo.html) |

| **Storage:** |                         |                                                  |
| ------------ | ----------------------- | ------------------------------------------------ |
|              | IDE Controller          | Realtek PCIE CardReader                          |
|              | Storage Controller      | Microsoft Storage Spaces Controller              |
|              | Storage Controller      | Standard NVM Express Controller                  |
|              | Disk Drive              | MTFDHBA1T0TDV-1AZ1AABHA  (1024 GB, PCI-E 3.0 x4) |
|              | SMART Hard Disks Status | OK                                               |

#### before 2022-06-01

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
	





