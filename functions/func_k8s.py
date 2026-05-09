import requests
import json
from config import token

'''
创建账号
kubectl get sa -A
kubectl create sa admin-token -n default
kubectl create clusterrolebinding admin-token --clusterrole=cluster-admin --serviceaccount=default:admin-token
kubectl get secret -n default $(kubectl get sa admin-token -n default -o jsonpath={.secrets[0].name}) -o jsonpath={.data.token} | base64 -d

kubectl describe secrets
kubectl describe secret prometheus-remote-token

kubectl config view --raw

# /api/v1/nodes
# /api/v1/pods
# /api/v1/namespaces
# /api/v1/services
# /api/v1/configmaps
# /apis/apps/v1/deployments
# /apis/apps/v1/statefulsets
# /apis/apps/v1/daemonsets
# /apis/apps/v1/replicasets
# /apis/networking.k8s.io/v1/ingresses
# /apis/networking.k8s.io/v1/networkpolicies
# /api/v1/persistentvolumes
# /api/v1/persistentvolumeclaims
# /api/v1/namespaces/{ns}/pods/{pod-name}
# /api/v1/namespaces/{ns}/pods/{pod-name}/log
# ?fieldSelector=status.phase=Running&pretty=false
# 发送 HTTP 请求（零证书、零文件、零写入）
'''

# ===================== 【你只需要填这里】 =====================
API_SERVER = "https://192.168.110.203:8443"

def getMasterList(search_key="master"):
    masterList = [
        {"name": "k8s-test-master", "desc": "测试环境k8s控制端", "server": API_SERVER},
    ]
    find_list = []
    for master in masterList:
        if search_key in master["name"] or search_key in master["desc"]:
            find_list.append(master)
    return "k8s API server列表："+ json.dumps(find_list)

def getNodeByServer(server):
    # 拼接请求头（核心：Bearer Token 认证，不依赖任何证书文件）
    headers = {
        "Authorization": f"Bearer {token}"
    }

    resp = requests.get(
        url=f"{server}/api/v1/nodes",
        headers=headers,
        verify=False,  # 跳过自签名证书
        timeout=10
    )
    resp_json = resp.json()
    items = resp_json.get('items', [])

    final_msgs = []
    final_msgs.append(f"总Node数量: {len(items)}")

    nodes = []
    for item in items:
        # 基本信息
        node_name = item["metadata"]["name"]

        labels = item.get("metadata", {}).get("labels", {})
        role_name = "WORKER"
        # 新 K8s 版本标签
        if "node-role.kubernetes.io/control-plane" in labels or "node-role.kubernetes.io/master" in labels:
            role_name = "MASTER"



        # 节点状态（Ready 或 NotReady）
        status = "Unknown"
        for cond in item["status"]["conditions"]:
            if cond["type"] == "Ready":
                status = cond["status"]

        # 节点 IP
        node_ip = ""
        for addr in item["status"]["addresses"]:
            if addr["type"] == "InternalIP":
                node_ip = addr["address"]

        # 内核 & OS
        kernel = item["status"]["nodeInfo"]["kernelVersion"]
        os = item["status"]["nodeInfo"]["osImage"]

        # CPU 容量
        cpu_total = item["status"]["capacity"]["cpu"]

        # 内存容量
        memory_total = item["status"]["capacity"]["memory"]

        # 容器运行时
        cri = item["status"]["nodeInfo"]["containerRuntimeVersion"]

        # Kubelet 版本
        kubelet = item["status"]["nodeInfo"]["kubeletVersion"]

        nodes.append({
            "name": node_name,
            "role": role_name,
            "status": status,
            "node_ip": node_ip,
            "kernel": kernel,
            "os": os,
            "cpu_total": cpu_total,
            "memory_total": memory_total,
            "cri": cri,
            "kubelet": kubelet
        })

    # Print table
    final_msgs.append("| # | Node名称 |    角色   |    状态   |  Node IP | 内核版本 | 操作系统 |   CPU  |   内存   | 容器运行时 | Kubelet 版本 |")
    final_msgs.append("|---|---------|-----------|-----------| ---------|--------|---------|--------|---------|----------|-------------|")
    for i, p in enumerate(nodes, 1):
        final_msgs.append(
            f"| {i} | {p['name'][:40]} | {p['role']} | {p['status']} | {p['node_ip']} | {p['kernel']} | {p['os']} | {p['cpu_total']} | {p['memory_total']} | {p['cri']} | {p['kubelet'][:50]} |")

    print("\n".join(final_msgs))
    # with open("nodes.json", "w") as f:
    #     json.dump(resp_json, f, indent=2)

    return "接口返回结果:\n"+ "\n".join(final_msgs)


def getPodByServer(server):
    # 拼接请求头（核心：Bearer Token 认证，不依赖任何证书文件）
    headers = {
        "Authorization": f"Bearer {token}"
    }

    resp = requests.get(
        url=f"{server}/api/v1/pods",
        headers=headers,
        verify=False,  # 跳过自签名证书
        timeout=10
    )
    resp_json = resp.json()
    items = resp_json.get('items', [])

    final_msgs = []

    final_msgs.append(f"总Pod数量: {len(items)}")

    ns_counts = {}
    status_counts = {}
    pods = []
    for item in items:
        name = item['metadata']['name']
        ns = item['metadata'].get('namespace', 'default')
        phase = item.get('status', {}).get('phase', 'Unknown')
        node = item.get('spec', {}).get('nodeName', 'N/A')
        pod_ip = item.get('status', {}).get('podIP', 'N/A')
        host_ip = item.get('status', {}).get('hostIP', 'N/A')
        ready = 'Unknown'
        for cond in item.get('status', {}).get('conditions', []):
            if cond['type'] == 'Ready':
                ready = cond['status']

        restarts = sum(cs.get('restartCount', 0) for cs in item.get('status', {}).get('containerStatuses', []))
        containers = item.get('spec', {}).get('containers', [])
        image = containers[0]['image'] if containers else 'N/A'
        if '/' in image:
            image_short = image.split('/')[-1]
        else:
            image_short = image
        ns_counts[ns] = ns_counts.get(ns, 0) + 1
        status_counts[phase] = status_counts.get(phase, 0) + 1
        pods.append({
            'name': name,
            'ns': ns,
            'phase': phase,
            'ready': ready,
            'node': node,
            'pod_ip': pod_ip,
            'host_ip': host_ip,
            'restarts': restarts,
            'image': image_short
        })

    # Print table
    final_msgs.append("| # | Pod名称 | Namespace | 状态 | Ready | Node | Pod IP | Host IP | 重启次数 | 镜像 |")
    final_msgs.append("|---|---------|-----------|------|-------|------|--------|---------|----------|------|")
    for i, p in enumerate(pods, 1):
        final_msgs.append(f"| {i} | {p['name'][:40]} | {p['ns']} | {p['phase']} | {p['ready']} | {p['node']} | {p['pod_ip']} | {p['host_ip']} | {p['restarts']} | {p['image'][:50]} |")
    final_msgs.append(f"\n--- 按Namespace统计 ---")
    for ns, count in sorted(ns_counts.items()):
        final_msgs.append(f"  {ns}: {count}个")

    final_msgs.append(f"\n--- 按状态统计 ---")
    for st, count in sorted(status_counts.items()):
        final_msgs.append(f"  {st}: {count}个")
    print("\n".join(final_msgs))

    # with open("pods.json", "w") as f:
    #     json.dump(resp_json, f, indent=2)


    return "接口返回结果:\n"+ "\n".join(final_msgs)


def getPodDetail(server, namespace, pod_name):
    # 拼接请求头（核心：Bearer Token 认证，不依赖任何证书文件）
    headers = {
        "Authorization": f"Bearer {token}"
    }

    resp = requests.get(
        url=f"{server}/api/v1/namespaces/{namespace}/pods/{pod_name}",
        headers=headers,
        verify=False,  # 跳过自签名证书
        timeout=10
    )
    resp_json = resp.json()
    return "接口返回结果:\n"+ json.dumps(resp_json)


if __name__ == '__main__':
    getPodDetail(server=API_SERVER, namespace="default", pod_name="lfms-kafka-779c7d8f79-pfflk")
    pass