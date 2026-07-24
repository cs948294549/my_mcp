# 华为交换机MSTP标准化配置模板
## 全局基础
stp mode mstp
stp region-configuration
 region-name NET-MSTP
 instance 1 vlan 10 11
 instance 2 vlan 20
 instance 3 vlan 99
 active

## 核心交换机（根桥）
stp instance 1 root primary
stp instance 2 root primary
stp instance 3 root primary

## 接入交换机下联端口
interface GigabitEthernet 0/0/1
 stp edged-port enable
 stp bpdu-protection