from functions.func_weather import get_weather, get_device_info,get_device_info2
from functions.func_runcmd import run_cmd, serverRunCMD
from functions.func_k8s import getMasterList, getNodeByServer, getPodByServer, getPodDetail


# --------------------------
# MCP 工具定义 (纯手写，不依赖 SDK)
# --------------------------
MCP_TOOLS_prompt = [
    {
        "name": "run_cmd",
        "description": "登录交换机设备执行命令，获取执行结果，注意区分设备类型",
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
        "name": "serverRunCMD",
        "description": "登录服务器执行命令，获取执行结果，注意区分设备类型，如果存在网域需要传入跳板机IP和端口，仅支持kubectl get/describe 和grep操作",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ip": {"type": "string", "description": "服务器IP"},
                "cmds": {"type": "array", "description": "需要执行的命令列表"},
                "jump_host": {"type": "string", "description": "跳板机地址，无法直连的机器需要跳板机转发"},
                "jump_port": {"type": "string", "description": "跳板机端口，默认是22"},
            },
            "required": ["ip", "cmds"]
        }
    },
    {
        "name": "get_device_info",
        "description": "通过设备名或者描述信息，在cmdb库中获取匹配的设备列表，获取设备IP地址",
        "inputSchema": {
            "type": "object",
            "properties": {
                "search_key": {"type": "string", "description": "关键字"},
            },
            "required": ["search_key"]
        }
    },
    # {
    #     "name": "get_k8s_server",
    #     "description": "调用接口时获取k8s控制器api地址",
    #     "inputSchema": {
    #         "type": "object",
    #         "properties": {
    #             "search_key": {"type": "string", "description": "关键字"},
    #         },
    #         "required": ["search_key"]
    #     }
    # },
    # {
    #     "name": "get_k8s_nodes",
    #     "description": "通过k8s控制器api查询k8s集群所有节点信息，使用/api/v1/nodes接口，需要使用get_k8s_server获取api地址",
    #     "inputSchema": {
    #         "type": "object",
    #         "properties": {
    #             "server": {"type": "string", "description": "k8s控制器api地址"},
    #         },
    #         "required": ["server"]
    #     }
    # },
    # {
    #     "name": "get_k8s_pods",
    #     "description": "通过k8s控制器api查询k8s集群所有pod信息，使用/api/v1/pods接口，需要使用get_k8s_server获取api地址",
    #     "inputSchema": {
    #         "type": "object",
    #         "properties": {
    #             "server": {"type": "string", "description": "k8s控制器api地址"},
    #         },
    #         "required": ["server"]
    #     }
    # },
    # {
    #     "name": "get_k8s_pod_detail",
    #     "description": "通过k8s控制器api查询指定的pod详情，使用/api/v1/namespaces/{namespace}/pods/{pod_name}接口，需要使用get_k8s_server获取api地址",
    #     "inputSchema": {
    #         "type": "object",
    #         "properties": {
    #             "server": {"type": "string", "description": "k8s控制器api地址"},
    #             "namespace": {"type": "string", "description": "namespace pod的命名空间"},
    #             "pod_name": {"type": "string", "description": "pod_name 指定的pod名称"},
    #         },
    #         "required": ["server"]
    #     }
    # },
]

MCP_TOOLS = {
    "run_cmd": run_cmd,
    "serverRunCMD": serverRunCMD,
    "get_device_info":get_device_info2,
    # "get_k8s_server":getMasterList,
    # "get_k8s_nodes":getNodeByServer,
    # "get_k8s_pods":getPodByServer,
    # "get_k8s_pod_detail":getPodDetail,
}

