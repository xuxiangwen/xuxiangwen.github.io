## Centos 7

### 安装Centos

1. 在http://isoredirect.centos.org/centos/7/isos/x86_64/列表中，打开一个镜像，下载CentOS-7-x86_64-DVD-xxxx.iso
2. 打开ultraiso，把iso刻录到U盘
3. u盘插入电脑，设置u盘优先启动
4. 安装centos。

### 创建用户

~~~shell
username=grid
adduser $username
passwd $username

# login again
~~~

### 添加用户到sudo列表中

~~~shell
su root
username=AUTH\\xu6
cat /etc/sudoer   # 检查是否已经设定了
sudo cp /etc/sudoer /etc/sudoer.`date +%Y-%m-%d`
chmod 640 /etc/sudoers
cat << EOF >> /etc/sudoers
$username    ALL=(ALL)       NOPASSWD: ALL
EOF

chmod 440 /etc/sudoers
tail -n 5 /etc/sudoers
ll /etc/sudoers

# login again
~~~

### 修改/etc/hostname

~~~shell
host_name=aa02
cat /etc/hostname   # 检查是否已经设定了

# 当前目录创建新的
cp /etc/hostname hostname 
sudo cat << EOF > hostname
$host_name
EOF

# 覆盖系统文件
sudo cp /etc/hostname /etc/hostname.`date +%Y-%m-%d`
sudo mv hostname /etc/hostname
sudo chown root:root /etc/hostname
sudo chmod 644 /etc/hostname
ll /etc/hostname
cat /etc/hostname

# restart 
sudo shutdown -r now
~~~

###  设置/etc/hosts

~~~shell
ll /etc/hosts
cat /etc/hosts 	# 检查是否已经设定了

# 当前目录创建新的

sudo cat << EOF > hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
15.15.175.163 aa00
15.15.174.155 aa01
15.15.173.21 aa02
15.15.174.117 aa03

EOF

# 覆盖系统文件
sudo cp /etc/hosts /etc/hosts.`date +%Y-%m-%d`
sudo mv hosts /etc/hosts
sudo chown root:root /etc/hosts
sudo chmod 644 /etc/hosts
ll /etc/hosts
cat /etc/hosts

~~~

> 对于windows，可以修改*C:\Windows\System32\drivers\etc\host*

### 创建id_rsa

~~~shell
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa

cat << EOF >> .ssh/authorized_keys
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC2zQnLXCdN0VREZ4uO2qGEoWOa0SUeLEsVRE1sQV854bn6X5oGzQnjor0YoLvcqBmCd0xhNLS6vKHEgkqKyLIXOQT5fzad6Zo0qBiKIhX0fojzYcgdOQA1tgvXxqpoBIodowNHJcXx2+EIfvPhgr1v35Hz7iTwdFK/Z3svsWCJxVi3jVfJXOiFLC/FFPqpgu/xML/40z2Z322r2vHSNG+YM0S2nb6Z2yU/jYldOQf1F40bYkPuCd5OCRdIxHpvStRoDB4c9c9XyxhPkzA2p0nOKAFAbFuTaBSviIUqJV6+QPg5pH5W1q5w2Z9n9Ugym5BkP9M+DfjDF6QTrosuWC3p grid@aa00
EOF

chmod 600 .ssh/authorized_keys
cat .ssh/authorized_keys
ll .ssh/authorized_keys
~~~

> 如果定义aa00，可以测试其对其它节点的访问权限
>
> ~~~shell
> #ssh的时候不会提示是否连接
> ssh-keyscan aa01 >> ~/.ssh/known_hosts 
> ssh-keyscan aa02 >> ~/.ssh/known_hosts 
> ssh-keyscan aa03 >> ~/.ssh/known_hosts 
> 
> ssh grid@aa01 hostname
> ssh grid@aa02 hostname
> ssh grid@aa03 hostname
> ~~~

### 笔记本盖子合上不休眠

~~~shell
grep -v '^#' /etc/systemd/logind.conf | grep -v '^$'
sudo sed -i "s|.*HandleLidSwitch=.*|HandleLidSwitch=lock|g" /etc/systemd/logind.conf
grep -v '^#' /etc/systemd/logind.conf | grep -v '^$'
sudo systemctl enable systemd-logind
sudo systemctl restart systemd-logind

# restart 
sudo shutdown -r now
~~~

### 关闭防火墙

~~~shell
sudo systemctl status firewalld.service
sudo systemctl stop firewalld
sudo systemctl disable firewalld.service
sudo systemctl status firewalld.service
~~~

### 安装vncserver

~~~
sudo yum -y install tigervnc-server 
sudo cp /lib/systemd/system/vncserver@.service /etc/systemd/system/vncserver@:1.service
sudo vi 
sudo sed -i "s|<USER>|$USER|g" /etc/systemd/system/vncserver@:1.service

sudo systemctl daemon-reload
sudo systemctl enable vncserver@:1.service
sudo systemctl restart vncserver@:1.service
# 这一步其实一直不能成功，所以还是需要调用vncserver :1启动远程桌面服务
sudo systemctl status vncserver@:1.service
sudo systemctl stop vncserver@:1.service


vncserver :1
vncserver -list
~~~

### 安装chrome

~~~
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
sudo yum localinstall -y google-chrome-stable_current_x86_64.rpm
~~~

### aa00上的磁盘挂载

Linux上任何块设备都不能直接访问，需挂载在目录上访问。挂载是指将额外文件系统与根文件系统某现存的目录建立起关联关系，进而使得此目录做为其它文件访问入口的行为（挂载的设备必须有文件系统）。详见[linux 磁盘管理三部曲](https://www.cnblogs.com/along21/p/7410619.html)。

~~~shell
sudo fdisk -l	# 查看有哪些磁盘
findmnt  # 查看所有设备挂载情况（树状结构显示）

# NTFS  磁盘映射
sudo yum install -y ntfs-3g

# 检查是否已经设定了
cat /etc/fstab   

# 当前目录创建新的
cp /etc/fstab fstab 
sudo cat << EOF >> fstab
/dev/sdb1               /home/grid/eipi10             xfs     defaults        0 0
/dev/sdc1               /home/grid/mount/c           ntfs-3g     defaults        0 0
/dev/sdc2               /home/grid/mount/d           ntfs-3g	     defaults        0 0
/dev/sdc3               /home/grid/mount/e           ntfs-3g     defaults        0 0
EOF

mkdir -p /home/grid/eipi10
mkdir -p /home/grid/mount/c
mkdir -p /home/grid/mount/d 
mkdir -p /home/grid/mount/e


# 覆盖系统文件
sudo cp /etc/fstab /etc/fstab.`date +%Y-%m-%d`
sudo mv fstab /etc/fstab
sudo chown root:root /etc/fstab
sudo chmod 644 /etc/fstab
ll /etc/fstab*
cat /etc/fstab


# restart 
sudo shutdown -r now
~~~

