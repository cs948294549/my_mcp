from flask import Flask, request, Response, jsonify
import json
from functools import wraps
from functions.mcp_interface import MCP_TOOLS, MCP_TOOLS_prompt
from functions.func_ldap import add_ad_user, delete_user
from config import VALID_OAUTH_TOKENS


app = Flask(__name__)

# ======================
# 2. OAuth2 认证装饰器
# ======================
def oauth2_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Unauthorized - Bearer token required"}), 401

        token = auth_header.split("Bearer ")[-1].strip()
        user = VALID_OAUTH_TOKENS.get(token)

        if not user:
            return jsonify({"error": "Unauthorized - invalid token"}), 401

        # 把用户信息传到视图函数
        request.user = user
        return f(*args, **kwargs)
    return decorated

# ======================
# 【关键】MCP 标准 OAuth 发现接口（解决 404）
# ======================
@app.route("/.well-known/oauth-authorization-server")
@app.route("/.well-known/openid-configuration")
def oidc_discovery():
    base_url = request.host_url.rstrip("/")
    return {
        "issuer": base_url,
        "token_endpoint": f"{base_url}/token",
        "authorization_endpoint": f"{base_url}/authorize",
        "response_types_supported": ["token"],
        "token_endpoint_auth_methods_supported": ["none"],
    }

@app.route("/.well-known/oauth-protected-resource")
def oauth_protected_resource():
    return jsonify({
        "resource": "mcp-server",
        "authorization_server": request.host_url + ".well-known/oauth-authorization-server"
    })

# --------------------------
# 核心端点
# --------------------------
@app.route("/mcp", methods=["GET", "POST"])
@app.route("/sse", methods=["GET", "POST"])
@oauth2_required
def sse_endpoint():
    if request.method == "POST":
        try:
            req_data = request.get_json(force=True)
        except Exception:
            return jsonify({"error": "Invalid JSON"}), 400

        resp_data = handle_mcp_request(req_data)
        print(request.user, "发送==sse==", resp_data)
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


# --------------------------
# LDAP业务接口代码
# --------------------------
@app.route("/ldap/add_user", methods=["POST"])
@oauth2_required
def ldap_add_user():
    try:
        data = request.json
        if not data:
            return {"code":1, "message": "data is empty", "data": {}}

        username = data.get('username', None)
        password = data.get('password', None)
        nickname = data.get('nickname', "未知")
        full_dn = data.get('full_dn', None)
        if full_dn is None or username is None or password is None:
            return {"code": 1, "message": "full_dn is None or username is None or password is None", "data": {}}

        user_info = {
            "username": username,
            "password": password,
            "nickname": nickname,
        }
        add_status = add_ad_user(user_info, full_dn)
        if add_status:
            return {"code":0, "message": "success", "data": {}}
        else:
            return {"code":1, "message": "failed", "data": {}}
    except Exception as e:
        return {"code":1, "message": "{}".format(str(e)), "data": {}}

@app.route("/ldap/del_user", methods=["POST"])
@oauth2_required
def ldap_del_user():
    try:
        data = request.json
        if not data:
            return {"code":1, "message": "data is empty", "data": {}}

        username = data.get('username', None)
        full_dn = data.get('full_dn', None)
        if full_dn is None or username is None:
            return {"code": 1, "message": "full_dn is None or username is None ", "data": {}}
        del_status = delete_user(username)
        if del_status:
            return {"code":0, "message": "success", "data": {}}
        else:
            return {"code":1, "message": "failed", "data": {}}
    except Exception as e:
        return {"code":1, "message": "{}".format(str(e)), "data": {}}

if __name__ == "__main__":
    print("Starting server on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
    # 加载证书和私钥
    # print("Starting server on http://0.0.0.0:5000")
    # ssl_context = ("server.crt", "server.key")
    # app.run(host="0.0.0.0", port=5000, ssl_context=ssl_context, debug=True)