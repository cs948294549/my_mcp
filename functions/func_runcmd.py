import requests
import json
from mcp_main.DebianDevice import DebianDevice
from config import user_password

def run_cmd(ip, cmds, vendor=None):
    if vendor and vendor.lower() == 'debian':
        dev = DebianDevice(ip, user_password["username"], user_password["password"])
        result = dev.exec_commands(cmds)
        if result!="failed":
            msgs = "执行参数：\n ip: {}\n cmds:{}\n执行结果:\n{}".format(ip, str(cmds), "\n".join(result.values()))
        else:
            msgs = "接口调用失败，需要检查服务"
    else:
        url = "http://192.168.170.252:8000/ssh/run_cmd"
        headers = {}

        filtered_cmds = []
        for cmd in cmds:
            if cmd.lower().startswith('display') or cmd.lower().startswith('dis'):
                filtered_cmds.append(cmd)
            else:
                return f"安全策略限制：只允许执行display开头的命令，当前命令 '{cmd}' 被拒绝"

        body = {
            "ip": ip,
            "cmds": filtered_cmds,
        }
        if vendor:
            body["vendor"] = vendor
        resp = requests.post(url, headers=headers, json=body)
        json_data = json.loads(resp.text)
        if json_data.get('code') == 0:
            _data = json_data.get('data')
            msgs = "执行参数：\n ip: {}\n cmds:{}\n执行结果:\n{}".format(_data.get('ip'), str(_data.get('cmds')), "\n".join(_data.get('result',{}).get('data').values()))
        else:
            msgs = "接口调用失败，需要检查服务"
    return msgs


if __name__ == '__main__':

    aa1 = run_cmd("47.98.235.241",["docker ps -a"], "debian")
    print(aa1)
