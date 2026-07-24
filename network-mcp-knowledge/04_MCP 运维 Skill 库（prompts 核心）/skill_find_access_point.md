# Skill Name: find_access_point
## 简介
通过调用交换机执行命令，快速定位所查询IP或MAC在网络中的接入位置
## 入参
ip/mac 二选一必填
## 执行步骤
1. 核心交换机执行 dis arp all | in {IP/MAC}，获取MAC地址
2. 执行 dis mac-add | in {MAC} 查询转发接口
3. 接口为聚合口则执行 dis eth-trunk{number} 获取物理口
4. 通过LLDP追踪上联交换机，逐级定位接入交换机端口
## 参考命令
dis arp all | include X.X.X.X
dis mac-address | include XXXX-XXXX-XXXX
## 异常判断
无ARP条目：终端离线；无MAC条目：流量未经过核心交换机