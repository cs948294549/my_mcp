# OpenELB EIP故障应急
1. 同网段机器无法ping EIP，但curl访问返回Nginx404
根因：Calico SNAT篡改源IP，ICMP回程阻断，TCP七层代理正常
2. ARP MAC全FF，二层应答异常
临时方案：调整iptables规避出站MASQUERADE
永久方案：修改Calico IPPool NAT策略