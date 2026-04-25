import requests
import json
from config import token

# ===================== 【你只需要填这里】 =====================
API_SERVER = "https://192.168.110.203:8443"



'''
创建账号
kubectl get sa -A
kubectl create sa admin-token -n default
kubectl create clusterrolebinding admin-token --clusterrole=cluster-admin --serviceaccount=default:admin-token
kubectl get secret -n default $(kubectl get sa admin-token -n default -o jsonpath={.secrets[0].name}) -o jsonpath={.data.token} | base64 -d
'''

def getPods():
    # 拼接请求头（核心：Bearer Token 认证，不依赖任何证书文件）
    headers = {
        "Authorization": f"Bearer {token}"
    }
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
    resp = requests.get(
        url=f"{API_SERVER}/api/v1/nodes?labelSelector=!node-role.kubernetes.io/master",
        headers=headers,
        verify=False,  # 跳过自签名证书
        timeout=10
    )
    print(json.dumps(resp.json(), indent=2))
    # with open("pressure_log_pod.json", "w") as f:
    #     f.write(json.dumps(resp.json(), indent=2))


if __name__ == '__main__':
    getPods()
    pass