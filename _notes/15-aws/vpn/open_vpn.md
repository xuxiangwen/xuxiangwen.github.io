# [OpenVPN 路由详解](https://limbo.moe/posts/2018/openvpn-routes)

理解 VPN 路由（以及任何网络路由）配置的关键是认识到一个 IP packet 如何被传输，以下描述的是极度简化后的单向传输过程：

1. 机器 A (`192.168.0.2`) 发送了IP packet到目标B（ `172.29.1.4` ） .
2. 根据本地路由规则，`172.29.1.0/24` 的下一跳是虚拟网卡 tun0, 由 VPN 客户端接管。
3. VPN 客户端将这个 packet 的来源地址从 `192.168.0.2` 改为 `10.8.0.123`, 转发给 VPN 服务端。
4. VPN 服务端收到 packet. 根据本地路由规则，`172.29.1.0/24` 的下一跳是默认网关 `172.29.0.1`.
5. 默认网关找到在同一个局域网内的机器 B (`172.29.1.4`).

~~~mermaid
graph TD; 
    A([A:192.168.0.2]) --> |`172.29.1.0/24` 的下一跳是虚拟网卡 tun0|tun0([tun0]);  
    tun0 --> |VPN Client接管|vpn_client([VPN Client]);
    vpn_client --> |修改source为10.8.0.123|vpn_server([VPN Server<br>]);
    vpn_server --> |`172.29.1.0/24` 的下一跳是默认网关 `172.29.0.1`|gateway1([Gateway:172.29.1.4]);
	gateway1 --> B([B:172.29.0.1]);

~~~

## 客户端 -> 内网

为什么机器 A 的本地路由表里会有 `172.29.1.0/24` 这个网段的路由规则？通常情况下，这是 VPN 服务端推送给客户端，由客户端在建立 VPN 连接时自动添加的。例如 `push "route 172.30.0.0 255.255.0.0"` 的作用就是将 `172.30.0.0/16` 网段的路由推送给客户端。

## 内网 -> 客户端

这个时候，如果机器 B 想要回复 A（比如发个 ACK），就会出问题，因为 packet 的来源地址还是 `10.8.0.123`, 而 `10.8.0.0/24` 网段并不属于当前局域网，是 VPN 服务端私有的——机器 B 往 `10.8.0.123` 发送的 ACK 会在某个位置（比如默认网关）遇到 "host unreachable" 而被丢弃。对于机器 A 来说，表面现象可能是连接超时或 ping 不通。

解决方法是，在 packet 离开 VPN 服务端时，将其「伪装」成来自 `172.29.0.3`（VPN 服务端的局域网地址），这样机器 B 发送的 ACK 就能顺利回到 VPN 服务端，然后发给机器 A. 这就是所谓的 SNAT, 在 Linux 系统中由 iptables 来管理，具体命令是：`iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE`.

## 客户端 -> 另一个客户端的内网

连接 OpenVPN 的两个 client 之间可以互相通信，这是因为服务端推送的路由里包含了对应的网段。但是想从 Client A 到达 Client B 所在局域网的其他机器，还需要额外的配置。因为 OpenVPN 服务端缺少 Client B 局域网相关的路由规则。

配置示例：

~~~python
# server.conf
## 给客户端推送 172.29.0.0/16 网段的路由
push "route 172.29.0.0 255.255.0.0" # client -> Client B

## 在 OpenVPN Server 上添加 172.29.0.0/16 网段的路由，
## 具体下一跳是哪里，由 client-config 里的 iroute 指定
route 172.29.0.0 255.255.0.0

## 启用 client-config, 目录里的文件名对应 client.crt 的 Common Name
client-config-dir /etc/openvpn/ccd

# /etc/openvpn/ccd/client-b
## 告诉 OpenVPN Server, 172.29.0.0/16 的下一跳应该是 client-b
iroute 172.29.0.0 255.255.0.0
~~~

## 内网与内网互访

在前两节所给的配置基础上，只需要再加一点配置，就能实现 OpenVPN 服务端所在局域网与客户端所在局域网的互访。配置内容是，在各自局域网的默认网关上添加路由，将对方局域网网段的下一跳设为 OpenVPN 服务端 / 客户端所在机器，同时用 iptables 配置相应的 SNAT 规则。

例如：

1. Cluster A 的路由表里添加 `172.31.0.0/16`, 下一跳为 `172.30.0.16` (cluster-a-relay).
2. Cluster B 路由表里添加 `172.30.0.0/16`, 下一跳为 `172.31.1.2` (cluster-b-relay).