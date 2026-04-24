# mcp_server
## 安装qwen-code
```text
npm install -g @qwen-code/qwen-code@latest
qwen --version
```
## 启动mcp服务
```text
python3 main.py
```
## 安装mcp方便调用
```text
qwen mcp add --name time-tcp --url http://127.0.0.1:8000/sse

检查是否成功
qwen mcp list
```

## config配置
```text
根目录下创建config.py文件
user_password = {"username": "xxx", "password": "xxx"}
```
# 接口准备
## 交换机命令执行接口
```text
需要准备run_cmd中的接口，方便调用执行命令
参考项目 https://github.com/cs948294549/agent_exporter 可快速对接
```

# skills主备
## skill配置方法
```text
在 ~/.qwen/skills/<技能名英文>/SKILL.md
qwen启动后会自动读取
```
## 查找设备位置接入点skill
```text
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
```