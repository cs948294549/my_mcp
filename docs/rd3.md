# k8s服务API
```text
# 1. 创建 ServiceAccount 账号
kubectl create sa chensong-token -n default

# 2. 创建和原权限完全一样的 ClusterRole
kubectl apply -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: chensong-token
rules:
- resources:
  - endpoints
  - nodes
  - pods
  - services
  verbs:
  - get
  - list
  - watch
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
  name: prometheus-remote-new-token
  namespace: default
  annotations:
    kubernetes.io/service-account.name: prometheus-remote-new
type: kubernetes.io/service-account-token
EOF

# 查询相关信息
kubectl describe secrets
kubectl describe secret prometheus-remote-token

kubectl config view --raw

kubectl describe clusterrole <role-name>

```