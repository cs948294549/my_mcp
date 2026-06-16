import paramiko
from io import StringIO
from config import pkey

class JumpDirectConnect:
    def __init__(self, jump_host, jump_port, jump_user, jump_pwd):
        self.jump_host = jump_host
        self.jump_port = jump_port
        self.jump_user = jump_user
        self.jump_pwd = jump_pwd
        self.jump_client = None
        self.jump_transport = None

    def connect_jump(self):
        # 登录跳板
        self.jump_client = paramiko.SSHClient()
        self.jump_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        private_key = paramiko.RSAKey.from_private_key(StringIO(pkey))
        # pkey = paramiko.RSAKey.from_private_key_file("/path/id_rsa")
        # self.jump_client.connect(..., pkey=pkey)
        self.jump_client.connect(
            hostname=self.jump_host,
            port=self.jump_port,
            username=self.jump_user,
            password=self.jump_pwd,
            pkey=private_key,
            timeout=10
        )
        self.jump_transport = self.jump_client.get_transport()

    def get_target_transport(self, target_host, target_port=22):
        """
        不创建本地端口，直接打开跳板直连目标的tcp通道
        返回目标机器的Transport对象，用于执行命令/交互式shell
        """
        # 核心：direct-tcpip 直接打通跳板->目标，无本地端口
        chan = self.jump_transport.open_channel(
            kind="direct-tcpip",
            dest_addr=(target_host, target_port),
            src_addr=("127.0.0.1", 0),
            timeout=10
        )
        # 使用通道作为底层流，新建Transport做目标SSH握手
        target_trans = paramiko.Transport(chan)
        target_trans.start_client()
        return target_trans

    def close(self):
        if self.jump_client:
            self.jump_client.close()


if __name__ == "__main__":
    # 1. 初始化跳板连接
    jump = JumpDirectConnect(
        jump_host="192.168.170.250",
        jump_port=2201,
        jump_user="root",
        jump_pwd=None
        # jump_pwd="hYwSm.yVu79aT6G"
    )
    jump.connect_jump()

    # 2. 直接获取目标传输通道（无本地端口）
    target_tp = jump.get_target_transport(target_host="172.30.0.8")

    # 3. 使用transport登录目标机器
    # target_pkey = paramiko.RSAKey.from_private_key_file("/path/id_rsa")
    # target_tp.auth_publickey(username="root", key=target_pkey)
    target_tp.auth_password(username="root", password="hYwSm.yVu79aT6G")

    # 4. 执行命令
    # 5. 交互式shell（可选）
    # shell_chan = target_tp.open_session()
    # shell_chan.get_pty()
    # shell_chan.invoke_shell()
    chan = target_tp.open_session()
    chan.get_pty()
    chan.invoke_shell()

    chan.sendall("hostname\n".encode("utf-8"))
    chan.settimeout(5)
    line_data = ""
    while True:
        try:
            line = chan.recv(1024)
            line_data += line.decode('utf-8', 'ignore').replace("\r", "")
        except Exception as e:
            break

    print(line_data)




    # 释放资源
    target_tp.close()
    jump.close()