# k8s服务API
```text
# 1. 创建 ServiceAccount 账号
kubectl create sa chensong-token -n default
kubectl delete sa chensong-token -n default

# 2. 创建和原权限完全一样的 ClusterRole
kubectl apply -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: chensong-token
rules:
# 核心资源（pod、svc、cm 等）apiGroups 为空字符串 ""
- apiGroups: [""]
  resources:
  - pods
  - pods/log
  - services
  - configmaps
  - secrets
  - endpoints
  - nodes
  - namespaces
  - persistentvolumes
  - persistentvolumeclaims
  verbs: ["get", "list", "watch"]

# apps 资源（deployment、statefulset 等）
- apiGroups: ["apps"]
  resources:
  - deployments
  - replicasets
  - statefulsets
  - daemonsets
  verbs: ["get", "list", "watch"]

# 网络资源
- apiGroups: ["networking.k8s.io"]
  resources:
  - ingresses
  - networkpolicies
  verbs: ["get", "list", "watch"]
EOF

# 3. 绑定角色到账号
kubectl create clusterrolebinding chensong-token-binding \
  --clusterrole=chensong-token \
  --serviceaccount=default:chensong-token

# 4. 创建永久 Token Secret
kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: chensong-token-secret
  namespace: default
  annotations:
    kubernetes.io/service-account.name: chensong-token
type: kubernetes.io/service-account-token
EOF

# 查询相关信息
kubectl describe secrets
kubectl describe secret prometheus-remote-token

kubectl config view --raw

kubectl describe clusterrole <role-name>


kubectl get sa | grep chensong
kubectl get clusterrole | grep chensong
kubectl get clusterrolebinding | grep chensong


```

sa.yaml
```text
apiVersion: v1
kind: ServiceAccount
metadata:
  name: chensong-sa
  namespace: default
```

clusterrole.yaml
```text
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: chensong-read-clusterrole
rules:
# 核心基础资源
- apiGroups: [""]
  resources:
  - pods
  - pods/log
  - services
  - configmaps
  - secrets
  - endpoints
  - nodes
  - namespaces
  - persistentvolumes
  - persistentvolumeclaims
  verbs: ["get", "list", "watch"]

# apps 应用资源
- apiGroups: ["apps"]
  resources:
  - deployments
  - replicasets
  - statefulsets
  - daemonsets
  verbs: ["get", "list", "watch"]

# 网络资源
- apiGroups: ["networking.k8s.io"]
  resources:
  - ingresses
  - networkpolicies
  verbs: ["get", "list", "watch"]

# 任务调度
- apiGroups: ["batch"]
  resources:
  - jobs
  - cronjobs
  verbs: ["get", "list", "watch"]
```

clusterrolebinding.yaml
```text
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: chensong-read-binding
subjects:
- kind: ServiceAccount
  name: chensong-sa
  namespace: default
roleRef:
  kind: ClusterRole
  name: chensong-read-clusterrole
  apiGroup: rbac.authorization.k8s.io
```

sa-token.yaml
```text
apiVersion: v1
kind: Secret
metadata:
  name: chensong-sa-token
  namespace: default
  annotations:
    kubernetes.io/service-account.name: chensong-sa
type: kubernetes.io/service-account-token
```
创建资源
```text
kubectl apply -f sa.yaml
kubectl apply -f clusterrole.yaml
kubectl apply -f clusterrolebinding.yaml
kubectl apply -f sa-token.yaml
```


kuboard创建token命令参考
```text
cat << EOF > kuboard-create-token.yaml
---
apiVersion: v1
kind: Namespace
metadata:
  name: kuboard

---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: kuboard-admin
  namespace: kuboard

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: kuboard-admin-crb
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: kuboard-admin
  namespace: kuboard

---
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
  annotations:
    kubernetes.io/service-account.name: kuboard-admin
  name: kuboard-admin-token
  namespace: kuboard
EOF

kubectl apply -f kuboard-create-token.yaml 
echo -e "\033[1;34m将下面这一行红色输出结果填入到 kuboard 界面的 Token 字段：\033[0m"
echo -e "\033[31m$(kubectl -n kuboard get secret $(kubectl -n kuboard get secret kuboard-admin-token | grep kuboard-admin-token | awk '{print $1}') -o go-template='{{.data.token}}' | base64 -d)\033[0m"
```