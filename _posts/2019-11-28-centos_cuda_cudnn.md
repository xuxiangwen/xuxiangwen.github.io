---
# generated from _notes/00-env/centos_cuda_cudnn.md

title: CentOS 7下安装CUDA 11.2.2
categories: deep-learning
date: 2019-11-28
---

本文将详述centos7环境下如何安装nvidia GPU driver, CUDA和cuDNN。这应该是第n次更新安装它们啦，总体上步骤没有太大变化，只是软件的版本有一些改变。和网上类似文章相比，本文中所有的shell命令都可以直接执行，不需要手工去修改文件，所以更加方便。下面看看要安装的内容：

- **nvidia GPU driver**：英伟达公司显卡驱动。要安装CUDA， cuDNN，这是必要的。  

- **CUDA（Compute Unified Device Architecture）**：是英伟达公司推出的一种基于新的并行编程模型和指令集架构的通用计算架构，它能利用英伟达GPU的并行计算引擎，比CPU更高效的解决许多复杂计算任务。

- **cuDNN（CUDA Deep Neural Network library）**：是NVIDIA打造的针对深度神经网络的加速库，是一个用于深层神经网络的GPU加速库。如果你要用GPU训练模型，cuDNN不是必须的，但是一般会采用这个加速库。 

首先验证GPU是否是CUDA兼容的。执行以下命令获得显卡信息，然后对照[CUDA GPUs](https://developer.nvidia.com/cuda-gpus)中的列表，搜寻GPU是否在其中。

~~~shell
lspci | grep -i nvidia
~~~

如果显卡不在其中，下面也不用看了。

本文安装的版本：

- NVidia显卡驱动：460.84
- CUDA:  11.2.2
- cuDNN:  8.2.1

## 1. [系统要求](https://docs.nvidia.com/cuda/archive/11.2.2/cuda-installation-guide-linux/index.html)

首先要保证操作系统符合CUDA 11.2的要求。

![image-20210610225057848](/assets/images/image-20210610225057848.png)

在centos7下安装，内核和centos的版本分别需要是3.10和7.7。使用下面命令检查。

~~~shell
uname -r                             
cat /etc/centos-release
~~~

如果版本不满足，需要执行以下命令，更新操作系统。

~~~shell
sudo yum clean all
sudo yum update
~~~

更新的时间可能会比较长，请耐性等待，一般都会顺利成功。万一发生错误，到网上找找方案，很快就能解决。

## 2. [软件更新](https://docs.nvidia.com/cuda/archive/11.2.2/cuda-installation-guide-linux/index.html#pre-installation-actions)

根据上节表格中的要求，安装或更新一些软件。

1. 验证系统内核版本和安装开发包。

   ~~~shell
   uname -r
   sudo yum install -y gcc gcc-c++ kernel-devel-$(uname -r) kernel-headers-$(uname -r)
   ~~~

2. 验证gcc的版本。

   ~~~shell
   gcc --version
   ~~~

   由于CUDA 11.3要求GCC的版本是6以上，下面是安装GCC7的脚本。

   ~~~
   sudo yum install centos-release-scl
   sudo yum install devtoolset-7
   # launch a new shell instance using the Software Collection scl tool:
   scl enable devtoolset-7 bash
   gcc --version
   ~~~

   如果重新登录，gcc版本还是原先的版本，所以在CUDA安装前，需要执行`scl enable devtoolset-7 bash`。

## 3. 安装NVidia显卡驱动

1.  根据要安装CUDA的版本，找到合适的显卡驱动。本次安装需要满足$\geq 460.32.03$。

   ![image-20210610205730396](/assets/images/image-20210610205730396.png)

2. 下载[nvidia驱动](https://www.nvidia.com/Download/index.aspx?lang=en-us)。

   ![image-20191214111408934](/assets/images/image-20191214111408934.png)

3. 检查当前驱动情况

   ~~~shell
   sudo yum install https://www.elrepo.org/elrepo-release-7.el7.elrepo.noarch.rpm
   sudo yum install nvidia-detect      # 安装nvida-detect
   nvidia-detect -v                    # 检测能够升级到的驱动器版本
   cat /proc/driver/nvidia/version     # 查看当前驱动版本
   ~~~

4. 卸载之前驱动。如果第一次安装，忽略。

   ~~~shell
   sudo /usr/bin/nvidia-uninstall
   ~~~

5. 屏蔽nouveau显卡驱动，把nvidiafb从屏蔽列表中移除。

   ~~~shell
   sudo rm -rf  disable-nouveau.conf
   cat << EOF > disable-nouveau.conf
   blacklist nouveau
   options nouveau modeset=0
   
   EOF
   
   sudo chown root:root disable-nouveau.conf
   sudo chmod 644 disable-nouveau.conf
   sudo mv disable-nouveau.conf /etc/modprobe.d/
   
   cat /etc/modprobe.d/disable-nouveau.conf
   ll /etc/modprobe.d/disable-nouveau.conf
   ~~~

6. 重建 initramfs 镜像。

   ~~~shell
   sudo mv /boot/initramfs-$(uname -r).img /boot/initramfs-$(uname -r).img.bak
   sudo dracut /boot/initramfs-$(uname -r).img $(uname -r)
   ~~~

7. 修改运行级别为文本模式。

   ~~~shell
   sudo systemctl set-default multi-user.target    #设置运行级别为文本模式
   sudo shutdown -r now
   ~~~

8. 安装驱动。

   ~~~shell
   lsmod | grep nouveau                            #查看nouveau是否已经禁用, 应该没有返回内容
   nvidia_run=NVIDIA-Linux-x86_64-460.84.run
   chmod 755 $nvidia_run
   sudo  ./$nvidia_run
   sudo systemctl set-default graphical.target     #设置运行级别回图形模式
   sudo systemctl get-default
   sudo shutdown -r now
   ~~~

   >安装选项:
   >
   >- dkms: yes
   >- 32位兼容: yes
   >- nvidia-xconfig: no

9. 检查安装。

   ~~~shell
   cat /proc/driver/nvidia/version    
   nvidia-smi
   ~~~

   ![image-20210610202019287](/assets/images/image-20210610202019287.png)

## 4. 安装CUDA

1. 卸载老版本

   ~~~shell
   sudo yum remove -y xorg-x11-drv-nvidia-libs #之前安装中，发现老版本的，删除后才正常
   sudo yum remove -y xorg-x11-drv-nvidia      #之前安装中，发现老版本的，删除后才正常
   sudo yum remove -y cuda-drivers
   sudo yum remove -y cuda
   ~~~

2. 安装

   在 [CUDA Download](https://developer.nvidia.com/cuda-11.2.2-download-archive) 选择合适的CUDA版本，选择了runfile（local），将会出现如下安装代码。

   ![image-20210610201659667](/assets/images/image-20210610201659667.png)

   ~~~shell
   scl enable devtoolset-7 bash
   gcc --version
   
   wget https://developer.download.nvidia.com/compute/cuda/11.2.2/local_installers/cuda_11.2.2_460.32.03_linux.run
   sudo sh cuda_11.2.2_460.32.03_linux.run
   ~~~

   当出现如下窗口时，按照下图勾选要安装的内容（不要勾选Driver，因为上节已经安装了更新的版本），然后选择`install`。

   ![image-20210611084943032](/assets/images/image-20210611084943032.png)

   下面是安装完后的信息。

   ![image-20210610212611453](/assets/images/image-20210610212611453.png)

3. 在.bashrc中添加参数。

   ~~~shell
   if ! grep "/usr/local/cuda/bin" ~/.bashrc
   then 
     echo                                                                    >> ~/.bashrc
     echo export PATH="\$PATH:/usr/local/cuda/bin"                           >> ~/.bashrc
     echo export CUDA_HOME=/usr/local/cuda                                   >> ~/.bashrc
     echo export LD_LIBRARY_PATH="/usr/local/cuda/lib64:\$LD_LIBRARY_PATH"   >> ~/.bashrc
   fi
   source ~/.bashrc
   ~~~

4. 安装验证

   ~~~shell
   head -5 /usr/local/cuda/version.json
   nvcc -V
   ~~~

   ![image-20210610212918587](/assets/images/image-20210610212918587.png)

5. 再次检查NVidia。如果出现报错，请返回`3. 安装nvida显卡驱动`中第5步，再次安装显卡驱动。

   ~~~shell
   cat /proc/driver/nvidia/version    
   nvidia-smi
   ~~~

## 5. 安装cuDNN

1. 下载cuDNN。打开[cuDNN](https://developer.nvidia.com/cudnn) ，登录以后，选择最新版本后，点击`cuDNN Library for Linux (X86_64)`链接进行下载。

   ![image-20210610213502841](/assets/images/image-20210610213502841.png)

2. 安装

   ~~~shell
   tar -xzvf cudnn-11.3-linux-x64-v8.2.1.32.tgz
   sudo cp cuda/include/cudnn*.h /usr/local/cuda/include 
   sudo cp -P cuda/lib64/libcudnn* /usr/local/cuda/lib64 
   $ sudo chmod a+r /usr/local/cuda/include/cudnn*.h /usr/local/cuda/lib64/libcudnn*
   ~~~

3. 安装验证

   ~~~shell
   cat /usr/local/cuda/include/cudnn_version.h | grep CUDNN_MAJOR -A 2  
   ~~~

   ![image-20210610215137971](/assets/images/image-20210610215137971.png)

## 6. 其它

### 修复vncserver

如果发生vncserver不能工作，可以尝试下面的方法。

如果使用vncserver进行远程桌面连接centos，当安装完nvidia驱动后，可能vncserver不能工作。其大概原因是默认的gnome和显卡驱动中opengl不兼容。所以只要在vncserver中使用另外一个桌面Xfce。

   ~~~
sudo yum groupinstall "Xfce" -y

cat << EOF > ~/.vnc/xstartup   
xrdb $HOME/.Xresources
startxfce4 &
EOF

#启动vncserver
vncserver :1    
   ~~~

## 参考

- [Centos7.4安装CUDA9.1](https://blog.veir.me/2018/03/17/centos7-install-cuda9/)
- [cuDNN安装向导](https://docs.nvidia.com/deeplearning/sdk/cudnn-install/index.html )
- [How to Install and Configure VNC Server on CentOS 7](https://vitux.com/centos-vnc-server/)

## 更新历史

- 2021-06-10
  - NVidia显卡驱动：460.84
  - CUDA:  11.2.2
  - cuDNN:  8.2.1
- 2020-05-19: 安装nvida显卡驱动修改了脚本
  - CUDA:  10.2.89 
  - cuDNN:  7.6.5
- 2019-11-28
  - CUDA:  10.2.89 
  - cuDNN:  7.6.5

