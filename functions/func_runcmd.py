import requests
import json
from utils.DebianDevice import DebianDevice
from config import user_password

def run_cmd(ip, cmds, vendor=None):
    if vendor and vendor.lower() == 'debian':
        dev = DebianDevice(ip, user_password["username"], user_password["password"])
        result = dev.exec_commands(cmds)
        if result!="failed":
            msgs = "执行参数：\n ip: {}\n cmds:{}\n执行结果:\n{}".format(ip, str(cmds), "\n".join(result.values()))
        else:
            msgs = "接口调用失败，需要检查服务"
    return msgs


if __name__ == '__main__':
    aa1 = run_cmd("47.98.235.241",["sudo docker ps -a"], "debian")
    print(aa1)
