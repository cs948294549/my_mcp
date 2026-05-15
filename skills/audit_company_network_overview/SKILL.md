---
name: audit_company_network_overview
description: "通过批量登录全网网络设备执行标准化查询命令，自上而下逐层盘点设备资产、VLAN 网段、路由拓扑、ACL 安全策略、LLDP 链路邻居及域间访问权限，完整梳理摸清公司整体网络架构、业务域划分与现存配置隐患"
---
# 公司整体网络架构全盘梳理
以核心交换机为起点，自上而下逐级盘点全网设备、链路、网段、路由、安全策略，完整还原企业网络全貌
## 可能用到的接口
1.get_device_info
2.run_cmd
## 执行步骤
1. 从核心设备开始查询
2. 执行设备基础信息查询，参考命令是 dis device man、dis version，收集设备型号、设备版本；
3. 查询设备上的 IP和VLAN 资源，参考命令是 dis ip int brief、dis vlan brie、dis arp all, 提取各 VLAN 对应业务网段、网关地址、在线终端 IP/MAC，标记冲突网段与闲置 VLAN；
4. 梳理设备路由架构，参考命令是 dis ip routing-table、dis cu | include route-static，梳理默认路由、静态路由路由走向；
5. 查询 LLDP 邻居链路，参考命令是 dis lldp nei brie，采集设备上下联关系、聚合口成员、物理链路层级；
6. 根据 LLDP 邻居列表，依次登录设备查询有记录的设备邻居，重复步骤 2-6，逐级梳理邻居信息；
7. 汇总梳理全量信息，输出网络设备资产台账、VLAN-IP 网段对照表、物理 & 逻辑拓扑链路、ACL 安全策略清单、网络架构现存隐患及优化整改建议。









