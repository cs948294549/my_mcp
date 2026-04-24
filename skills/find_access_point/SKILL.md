---
name: find_access_point
description: "通过调用交换机执行命令mcp，快速定位所查询IP或MAC在网络中的接入位置"
---
# 设备接入位置定位
根据输入的IP或MAC地址，从核心交换机从上往下查找接入点
## 可能用到的接口
1.get_device_info
2.run_cmd
## 执行步骤
1. 首先到核心交换机上查询输入的IP或MAC是否存在，参考命令是 dis arp all | in {IP/MAC};
2. 在核心交换机上根据查询到的结果提取MAC地址，查询MAC地址转发接口，参考命令 dis mac-add | in {MAC};
3. 当查出来的接口名称是聚合口时，需要再查询物理口信息，参考命令 dis eth-trunk{number};
4. 根据查询到的物理转发接口，查询LLDP邻居关系，参考命令 dis lldp nei brie，提取出邻居设备名称；
4. 登录邻居设备重复步骤2、3、4，直到查不到邻居关系，证明接入点已经查到；
3. 总结信息，返回接入点位置以及途径的设备列表。