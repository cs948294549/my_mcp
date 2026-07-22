---
name: config_k8s_nginx
description: "配置k8s nginx pod内部的nginx配置，包含多种环境，主要入口在k8s master节点，主要内容是去拉取配置到本地，然后修改对应配置"
---
# 配置k8s nginx配置
根据输入的环境找到对应的k8s master节点，去获取对应的配置
## 可能用到的接口
1.get_device_info 获取设备信息
2.serverRunCMD 登录服务器执行kubectl命令
## 执行步骤
1. 首先到k8s master节点上查询nginx pod是否存在,参考命令 kubectl get pods ;
2. 查询nginx pod所使用的configmap是什么，参考命令 kubectl get deployment {nginx pod name} -o yaml  ;
3. 执行命令查询配置，将配置拉取到本地，写入本地文件*.conf，注意写入的时候使用utf-8字符，不需要修改成yaml文件，参考命令 kubectl get configmap {configmap name} -n default -o jsonpath='{.data.nginx\.conf}';
4. 最后根据需求，生成新配置，注意保留原始配置和新配置两份文件。