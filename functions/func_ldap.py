# 加在 import ldap3 之前
from Crypto.Hash import MD4
import hashlib

# 猴子补丁：让 hashlib 能找到 md4
hashlib.md4 = lambda data=b'': MD4.new(data)
hashlib.new = lambda name, data=b'': MD4.new(data) if name.lower() == 'md4' else hashlib._new(name, data)


from ldap3 import Server, Connection, ALL, NTLM, SUBTREE, LEVEL,BASE
from config import ADMIN_USER, ADMIN_PASS

# ===================== 你的域信息（改成你自己的） =====================
DOMAIN = "DK.com"
DC_SERVER = "192.168.110.193"  # 域控IP
LDAP_PORT = 389 # 明文389，LDAPS 636
# 根域名（必须正确！）
ROOT_DN = "DC=DK,DC=COM"



def get_ldap_conn():
    """获取LDAP连接"""
    # 创建服务对象
    server = Server(DC_SERVER, port=LDAP_PORT, get_info=ALL)
    # 建立连接，简单认证
    conn = Connection(
        server,
        user=f"DK\\{ADMIN_USER}",
        password=ADMIN_PASS,
        authentication=NTLM,
        auto_bind=True
    )
    conn.start_tls()
    if not conn.bound:
        raise Exception("LDAP 连接/认证失败")
    return conn

def check_ou_exists(ou_full_dn: str) -> bool:
    try:
        conn = get_ldap_conn()
        base = f"{ou_full_dn},{ROOT_DN}"
        conn.search(base, "(objectClass=organizationalUnit)", search_scope=BASE)
        res = len(conn.entries) > 0
        conn.unbind()
        return res
    except:
        return False

def check_ad_user(username: str):
    try:
        conn = get_ldap_conn()
        flt = f"(&(objectClass=user)(sAMAccountName={username}))"
        conn.search(ROOT_DN, flt, search_scope=SUBTREE)
        if len(conn.entries) > 0:
            full_dn = conn.entries[0].entry_dn
            exists = True
        else:
            full_dn = ""
            exists = False
        conn.unbind()
        return exists, full_dn
    except Exception as e:
        print(e)
        return False, ""

def add_ou(full_dn: str) -> bool:
    try:
        conn = get_ldap_conn()
        ou_list = full_dn.split(",")
        current_dn = []
        while len(ou_list) > 0:
            _dt = ou_list.pop()
            if "OU=" in _dt:
                current_dn.insert(0, _dt)
            ps = check_ou_exists(",".join(current_dn))
            if ps is False:
                _pwd_dn = ",".join(current_dn) + f",{ROOT_DN}"
                ou_success = conn.add(
                    _pwd_dn,
                    attributes={"ou": current_dn[0].replace("OU=", "").strip()},
                    object_class=["top", "organizationalUnit"]
                )
        return True
    except Exception as e:
        print(e)
        return False

def add_ad_user(user_info, dn: str) -> bool:
    try:
        conn = get_ldap_conn()
        username = user_info["username"]
        cn_name = user_info["nickname"]
        password = user_info["password"]

        is_exist, get_user_dn = check_ad_user(user_info["username"])
        if is_exist:
            print("更新密码")
            user_dn = f"CN={cn_name},{dn},{ROOT_DN}"
            if get_user_dn.upper()==user_dn.upper():
                password = user_info["password"]
                # AD 密码固定编码格式
                pwd_encoded = f'"{password}"'.encode("utf-16-le")
                changes = {
                    "unicodePwd": (2, [pwd_encoded])
                }
                success = conn.modify(get_user_dn, changes)
                print(f"密码重置结果: {success}")
                conn.unbind()
                return success
            else:
                print(f"分组不匹配")
                return False
        else:
            print("新增用户")
            add_ou(full_dn=dn)
            user_dn = f"CN={cn_name},{dn},{ROOT_DN}"

            attributes = {
                "cn": cn_name,
                "sn": cn_name,
                "givenName": cn_name,
                "displayName": cn_name,
                "sAMAccountName": username,
                "userPrincipalName": f"{username}@{DOMAIN}",
                "userAccountControl": 512,
                "unicodePwd": f'"{password}"'.encode("utf-16-le")
            }

            # 创建用户
            success = conn.add(
                user_dn,
                attributes=attributes,
                object_class=["top", "person", "organizationalPerson", "user"]
            )

            if success:
                print(f"✅ 用户创建成功：{user_dn}")
                return True
            else:
                print(f"❌ 用户创建失败：{conn.result}")
                return False
    except Exception as e:
        print(e)
        return False


def delete_user(username: str) -> bool:
    try:
        conn = get_ldap_conn()
        is_exist, full_dn = check_ad_user(username)
        if is_exist:
            print("删除用户")
            conn.delete(full_dn)
        else:
            print("用户不存在")
        conn.unbind()
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    # 新增和修改用户
    u_info = {
        "username": "zhangsan",
        "password": "Admin@12345",
        "nickname": "张三",
    }
    d = add_ad_user(u_info,dn="OU=产品规划管理组,OU=底座及能力研究室01,OU=平台软件开发部,OU=航天时代低空科技")
    print(d)

    # 删除用户
    # delete_user(username="chensong1")
    pass

