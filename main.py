from flask import Flask, request, Response, jsonify
import json
from functions.func_weather import get_weather, get_device_info
from functions.func_runcmd import run_cmd
from functions.func_k8s import getMasterList, getNodeByServer, getPodByServer
app = Flask(__name__)

# --------------------------
# 状态管理
# --------------------------


# --------------------------
# MCP 工具定义 (纯手写，不依赖 SDK)
# --------------------------
MCP_TOOLS_prompt = [
    {
        "name": "run_cmd",
        "description": "登录交换机设备执行命令，获取执行结果",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ip": {"type": "string", "description": "交换机IP"},
                "cmds": {"type": "array", "description": "需要执行的命令列表"},
                "vendor": {"type": "string", "description": "设备厂商，没有获取到具体的信息就不填"},
            },
            "required": ["ip", "cmds"]
        }
    },
    {
        "name": "get_device_info",
        "description": "通过设备名或者描述信息，返回匹配的设备列表，获取设备IP地址",
        "inputSchema": {
            "type": "object",
            "properties": {
                "search_key": {"type": "string", "description": "关键字"},
            },
            "required": ["search_key"]
        }
    },
    {
        "name": "get_k8s_server",
        "description": "通过设备名或者描述信息，返回k8s控制器api地址",
        "inputSchema": {
            "type": "object",
            "properties": {
                "search_key": {"type": "string", "description": "关键字"},
            },
            "required": ["search_key"]
        }
    },
    {
        "name": "get_k8s_nodes",
        "description": "通过k8s控制器api查询k8s集群所有节点信息，使用/api/v1/nodes接口",
        "inputSchema": {
            "type": "object",
            "properties": {
                "server": {"type": "string", "description": "k8s控制器api地址"},
            },
            "required": ["server"]
        }
    },
    {
        "name": "get_k8s_pods",
        "description": "通过k8s控制器api查询k8s集群所有pod信息，使用/api/v1/pods接口",
        "inputSchema": {
            "type": "object",
            "properties": {
                "server": {"type": "string", "description": "k8s控制器api地址"},
            },
            "required": ["server"]
        }
    },
]

MCP_TOOLS = {
    "run_cmd": run_cmd,
    "get_device_info":get_device_info,
    "get_k8s_server":getMasterList,
    "get_k8s_nodes":getNodeByServer,
    "get_k8s_pods":getPodByServer,
}


# --------------------------
# 核心端点
# --------------------------
@app.route("/sse", methods=["GET", "POST"])
def sse_endpoint():
    if request.method == "POST":
        try:
            req_data = request.get_json(force=True)
        except Exception:
            return jsonify({"error": "Invalid JSON"}), 400

        resp_data = handle_mcp_request(req_data)
        print("发送==sse==", resp_data)
        return jsonify(resp_data)


# --------------------------
# MCP 逻辑纯手写实现
# --------------------------
def handle_mcp_request(req):
    method = req.get("method")
    req_id = req.get("id")
    print("收到消息==sse==", req)
    if method == "initialize":
        return {
            "jsonrpc": "2.0", "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "my-server", "version": "1.0.0"}
            }
        }
    elif method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    elif method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": MCP_TOOLS_prompt}}
    elif method == "tools/call":
        func_params = req.get("params", {})

        func_name = func_params.get("name", "")
        if func_name in MCP_TOOLS:
            result = MCP_TOOLS[func_name](**func_params.get("arguments", {}))
            return {
                "jsonrpc": "2.0", "id": req_id,
                "result": {"content": [{"type": "text", "text": result}]}
            }
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "tool Not found"}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Not found"}}


if __name__ == "__main__":
    print("Starting server on http://0.0.0.0:8000")
    app.run(host="0.0.0.0", port=8000, debug=True)