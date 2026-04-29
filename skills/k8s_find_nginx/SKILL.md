---
name: find_k8s_nginx
description: "只知道服务端口号, 通过调用执行命令mcp，逆向快速查询k8s发布的nginx配置"
---
# K8s 只知道「端口号」，完整逆向排查流程
核心逻辑：端口 → 找到 Service → 找到关联 Pod/Deployment → 看挂载 ConfigMap / 配置 / 容器参数
## 可能用到的MCP接口
1.get_device_info
2.run_cmd
## 执行步骤
1. 通过端口查出Service名称以及命名空间ns,deploy名称是Service名称的前缀,参考命令 kubectl get svc -A | grep {端口号};
2. 找到对应的configmap名称, 参考命令 kubectl get deploy {deploy名称} -n {命名空间ns} -o jsonpath='{.spec.template.spec.volumes[*].configMap.name}';
3. 查看配置内容kubectl get configmap {configmap名称} -n {命名空间ns} -o yaml