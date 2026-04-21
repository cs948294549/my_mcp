# mcp_server
## 安装qwen-code
```text
npm install -g @qwen-code/qwen-code@latest
qwen --version
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
