### Shell 日期格式化

~~~shell
date '+%Y%m%d_%H%M%S'
~~~

ll命令

~~~shell
alias ll='ls -l --color=auto'
~~~

### Tree用法示例

- 常规用法

    ~~~shell
    tree -fDpugsh
    ~~~

    - f: 显示文件全路径
    - D: 显示最后的修改时间
    - p：显示文件的模式（chmod）
    - u：显示用户
    - g：显示group
    - s：显示文件大小
    - h：以可读方式显示size
    
- 显示目录

    ~~~shell
    tree -fDpugshd  
    ~~~

    - d： 仅仅显示目录

- 仅仅显示文件

    ~~~shell
    tree -fDpugshF  | grep -v /$
    ~~~

    - F: Appends '/', '=', '*', '@', '|' or '>' as per ls -F. 对于目录会添加一个/

### 时间同步

~~~shell
sudo timedatectl set-ntp yes
sudo timedatectl set-time '2020-02-28 17:47:20'
~~~

### 集群同步时间

~~~shell
#chrony 时间同步  
#http://www.ywnds.com/?p=6079
#
source ~/cluster-install/config.`hostname`
pdsh -R ssh -w $user@$servers sudo yum install chrony
pdsh -R ssh -w $user@$servers sudo systemctl start chronyd.service
pdsh -R ssh -w $user@$servers sudo systemctl enable chronyd.service
pdsh -R ssh -w $user@$servers sudo systemctl status chronyd.service


sudo vim /etc/chrony.conf
#in server
local stratum 10
allow 15.15.165.218
allow 15.15.165.35
allow 15.15.166.231
allow 15.15.166.234

#in client
server 15.15.165.218 iburst
allow 15.15.165.218
allow 15.15.165.35
allow 15.15.166.231
allow 15.15.166.234

sudo systemctl restart chronyd.service
chronyc sources -v
chronyc sourcestats -v

pdsh -R ssh -w $user@$servers chronyc sources -v
pdsh -R ssh -w $user@$servers date
pdsh -R ssh -w $user@$servers timedatectl   
~~~

### SELinux

安全增强型 Linux（Security-Enhanced Linux）简称 SELinux，它是一个 Linux 内核模块，也是 Linux 的一个安全子系统。SELinux 主要由美国国家安全局开发。2.6 及以上版本的 Linux 内核都已经集成了 SELinux 模块。开启SELinux有时会占用大量内存和CPU资源，所以可以选择关闭。

查看状态

~~~shell
sestatus -v
~~~

临时关闭

~~~shell
sudo setenforce 0  
~~~

永久关闭

~~~shell
sudo sed -i 's/^SELINUX=.*/SELINUX=disabled/g'  /etc/selinux/config
~~~

### 重新生成/var/log/messages

~~~shell
sudo rm -rf /var/log/messages
sudo systemctl restart rsyslog.service
sudo schmod 644 /var/log/messages
~~~

