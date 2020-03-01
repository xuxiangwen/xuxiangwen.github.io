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

