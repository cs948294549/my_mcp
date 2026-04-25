# mcp_server
## 安装qwen-code
```text
安装qwen-code
npm install -g @qwen-code/qwen-code@latest
qwen --version

安装claude-code
https://www.runoob.com/claude-code/claude-code-install.html
npm install -g @anthropic-ai/claude-code
claude-code --version
```
## 启动mcp服务
```text
python3 main.py
```
## 安装mcp方便调用
```text
qwen code安装mcp
qwen mcp add --name <名称> --url http://127.0.0.1:8000/sse
检查是否成功
qwen mcp list

claude code安装mcp
claude mcp add --transport http <名称> http://127.0.0.1:8000/sse
检查是否成功
claude mcp list

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
# 额外插件
## windows
```text
windows好点的终端
https://github.com/microsoft/terminal/releases
https://github.com/microsoft/terminal
winget install --id Microsoft.WindowsTerminal -e
```

# 一个完整示例
```text
claude code
❯ 帮我查下192.168.120.65 接在哪个交换机下

● Skill(find_access_point)
  ⎿  Successfully loaded skill

● 我来帮你追踪 192.168.120.65 的接入位置。首先查找核心交换机。

  Called notion 2 times (ctrl+o to expand)

● 找到两台核心交换机，先在两台核心上查询 ARP 信息。

  Called notion 2 times (ctrl+o to expand)

● 找到了！MAC 地址是 d0f4-0536-ae17，转发接口是 Eth-Trunk3。接下来查询 MAC 地址表和 Eth-Trunk 成员口。

  Called notion 2 times (ctrl+o to expand)

● MAC 在 Eth-Trunk3 上，包含两个成员口 XGE0/0/5 和 XGE1/0/5。接下来查询 LLDP 邻居，看 Eth-Trunk3 连接到哪台设备。

  Called notion 2 times (ctrl+o to expand)

● 没有匹配到，让我查看完整的 LLDP 邻居表。

  Called notion 2 times (ctrl+o to expand)

● 从 LLDP 可以看到，XGE0/0/5 和 XGE1/0/5（Eth-Trunk3 的成员口）都连接到 DK-35F-A003。接下来登录 DK-35F-A003 查询 MAC
  地址。

  Called notion 3 times (ctrl+o to expand)

● 找到了！MAC 地址 d0f4-0536-ae17 在 DK-35F-A003 的 GE0/0/16 端口上学习到。让我确认一下这个端口是否还有下游设备。

  Called notion (ctrl+o to expand)

∴ Thinking…

  No neighbor device found on GE0/0/16 - it shows "-" for Neighbor Dev, which means the device connected there doesn't
  support LLDP or has it disabled. This is likely an endpoint device (PC/server). The path ends here.
● 追踪完毕！以下是结果汇总：

  接入点位置

  ┌────────────┬───────────────────────────┐
  │    项目    │           信息            │
  ├────────────┼───────────────────────────┤
  │ 终端 IP    │ 192.168.120.65            │
  ├────────────┼───────────────────────────┤
  │ 终端 MAC   │ d0f4-0536-ae17            │
  ├────────────┼───────────────────────────┤
  │ 接入交换机 │ DK-35F-A003 (10.92.42.83) │
  ├────────────┼───────────────────────────┤
  │ 接入端口   │ GE0/0/16                  │
  └────────────┴───────────────────────────┘

  路径

  1. DK-IDC-Center (核心交换机 10.92.42.64) → Eth-Trunk3 (成员口 XGE0/0/5, XGE1/0/5)
  2. DK-35F-A003 (接入交换机 10.92.42.83) → GE0/0/16 → 终端设备

  GE0/0/16 端口没有 LLDP 下游邻居，说明该端口直接连接终端设备，即为最终接入点。

✻ Worked for 1m 5s

!!! 一轮消耗接近20Wtoken
```