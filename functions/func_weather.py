import json


def get_weather(city):
    return f"{city}：晴天 25°C"


def get_device_info(search_key):
    device_list = [
        {"ip": "47.98.235.241", "name": "aliyun_host", "desc": "我的云主机", "vendor":"debian"},
        {"ip": "10.92.42.64", "name":"DK-IDC-Center", "desc": "核心交换机"},
        {"ip": "10.92.42.60", "name": "DK-35F-DC-Management", "desc": "带外交换机"},
        {"ip": "10.92.42.61", "name": "DK-35F-DC-Management-B", "desc": "带外交换机扩展"},
        {"ip": "10.92.42.66", "name": "DK-35F-DC-VMStack", "desc": "业务交换机"},
        {"ip": "10.92.42.67", "name": "DK-35F-DC-VMSack-B", "desc": "业务交换机扩展"},
        {"ip": "10.92.42.80", "name": "DK-35F-Aceess-Office", "desc": "35F接入交换机"},
        {'ip': '10.92.42.81', 'name': 'DK-35F-A001', 'desc': '35F接入交换机1'},
        {'ip': '10.92.42.82', 'name': 'DK-35F-A002', 'desc': '35F接入交换机2'},
        {'ip': '10.92.42.83', 'name': 'DK-35F-A003', 'desc': '35F接入交换机3'},
        {'ip': '10.92.42.84', 'name': 'DK-35F-A004', 'desc': '35F接入交换机4'},
        {'ip': '10.92.42.85', 'name': 'DK-35F-A005', 'desc': '35F接入交换机5'},
        {'ip': '10.92.42.86', 'name': 'DK-35F-A006', 'desc': '35F接入交换机6'},
        {'ip': '10.92.42.87', 'name': 'DK-35F-A007', 'desc': '35F接入交换机7'},
        {'ip': '10.92.42.88', 'name': 'DK-35F-A008', 'desc': '35F接入交换机8'},
        {'ip': '10.92.42.89', 'name': 'DK-35F-A009-POE', 'desc': '35F接入交换机9'},
        {'ip': '10.92.42.90', 'name': 'DK-22F-Office-Center', 'desc': '22F核心交换机'},
        {'ip': '10.92.42.91', 'name': 'DK-22F-Area-001', 'desc': '22F接入交换机1'},
        {'ip': '10.92.42.92', 'name': 'DK-22F-Area-002', 'desc': '22F接入交换机2'},
        {'ip': '10.92.42.93', 'name': 'DK-22F-Area-003', 'desc': '22F接入交换机3'},
        {'ip': '10.92.42.94', 'name': 'DK-22F-Area-004', 'desc': '22F接入交换机4'},
        {'ip': '10.92.42.95', 'name': 'DK-22F-Area-005', 'desc': '22F接入交换机5'},
    ]
    find_devs = []
    for device in device_list:
        if search_key in device["name"] or search_key in device["desc"]:
            find_devs.append(device)
    if len(find_devs) == 0:
        return "未查找到设备"
    else:
        return "设备列表："+ json.dumps(find_devs)