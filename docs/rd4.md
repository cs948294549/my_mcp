服务器iptable基础配置
```text
-A INPUT -p tcp -m tcp --dport 9090 -j ACCEPT
-A INPUT -s 192.168.130.51/32 -j ACCEPT
-A INPUT -j white_list
-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
-A INPUT -p icmp -j ACCEPT
-A INPUT -i lo -j ACCEPT
-A INPUT -i br-391cb3c30c8c -j ACCEPT
-A INPUT -i docker0 -j ACCEPT
-A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT
-A INPUT -j REJECT --reject-with icmp-host-prohibited


iptables -I INPUT -s 192.168.130.51/32 -j ACCEPT
iptables -A white_list -s 192.168.120.19/32 -p tcp -m tcp --dport 8800 -j ACCEPT
iptables -A white_list -s 192.168.120.141/32 -p tcp -m tcp --dport 8800 -j ACCEPT
iptables -A white_list -s 192.168.130.18/32 -p tcp -m tcp --dport 8800 -j ACCEPT
iptables -A white_list -s 192.168.130.17/32 -p tcp -m tcp --dport 8800 -j ACCEPT
iptables -A white_list -s 192.168.130.14/32 -p tcp -m tcp --dport 8800 -j ACCEPT
iptables -A white_list -s 192.168.130.11/32 -p tcp -m tcp --dport 8800 -j ACCEPT
iptables -A white_list -s 192.168.170.252/32 -j ACCEPT
iptables -A white_list -p tcp -m tcp --dport 8443 -j ACCEPT
-A white_list -j RETURN


```