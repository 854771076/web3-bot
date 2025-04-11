import base64
import binascii
import random

import rsa
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def process_string(t, e):
    # Step 1: 处理 e 的最后两个字符，转换为数字
    n = e[-2:]
    r = []
    for char in n:
        o = ord(char)
        r.append(o - 87 if o > 57 else o - 48)

    # Step 2: 计算 n
    n = 36 * r[0] + r[1]

    # Step 3: 初始化其他变量
    a = round(t) + n
    _ = [[] for _ in range(5)]  # 创建五个空列表
    c = {}
    u = 0

    # Step 4: 对 e 进行处理并分组
    e = e[:-2]  # 删除 e 的最后两个字符
    for s in e:
        if s not in c:
            c[s] = 1
            _[u].append(s)
            u = 0 if u == 4 else u + 1  # u 0-4 循环

    # Step 5: 随机选取字符并构造结果
    f = a
    d = 4
    p = ""
    g = [1, 2, 5, 10, 50]

    while f > 0:
        if f >= g[d]:
            h = random.randint(0, len(_[d]) - 1)
            p += _[d][h]
            f -= g[d]
        else:
            _.pop(d)
            g.pop(d)
            d -= 1

    return p


def e4(t, e):
    # 位操作：右移 e 位后，提取出第 e 位
    return (t >> e) & 1


def e3(t):
    # 字符集：返回字符
    e = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789()"
    return '.' if t < 0 or t >= len(e) else e[t]


def e2(t):
    # 处理字节序列 t，进行位操作并返回结果
    n = ""
    r = ""
    s = len(t)

    # 嵌套的位操作函数
    def process(t, e):
        n = 0
        for r in range(23, -1, -1):  # 24 - 1 = 23
            if e4(e, r) == 1:
                n = (n << 1) + e4(t, r)
        return n

    for a in range(0, s, 3):
        if a + 2 < s:
            _ = (t[a] << 16) + (t[a + 1] << 8) + t[a + 2]
            n += e3(process(_, 7274496)) + e3(process(_, 9483264)) + e3(process(_, 19220)) + e3(process(_, 235))
        else:
            c = s % 3
            if c == 2:
                _ = (t[a] << 16) + (t[a + 1] << 8)
                n += e3(process(_, 7274496)) + e3(process(_, 9483264)) + e3(process(_, 19220))
                r = "."
            elif c == 1:
                _ = t[a] << 16
                n += e3(process(_, 7274496)) + e3(process(_, 9483264))
                r = ".."

    return {'res': n, 'end': r}


def e1(t):
    # 获取 e2 的结果，并返回拼接后的字符串
    result = e2(t)
    return result['res'] + result['end']


class Rsa:
    def __init__(self):
        e = '010001'
        e = int(e, 16)
        n = '00C1E3934D1614465B33053E7F48EE4EC87B14B95EF88947713D25EECBFF7E74C7977D02DC1D9451F79DD5D1C10C29ACB6A9B4D6FB7D0A0279B6719E1772565F09AF627715919221AEF91899CAE08C0D686D748B20A3603BE2318CA6BC2B59706592A9219D0BF05C9F65023A21D2330807252AE0066D59CEEFA5F2748EA80BAB81'
        n = int(n, 16)
        self.pub_key = rsa.PublicKey(e=e, n=n)

    def Rencrypt(self, pwd):
        text = rsa.encrypt(pwd.encode(), self.pub_key)
        return text.hex()


class Cbc:
    def __init__(self, key, iv):
        # 初始化密钥
        self.key = key
        self.iv = iv
        # 初始化数据块大小
        self.length = AES.block_size
        # 截断函数，去除填充的字符
        self.unpad = lambda date: date[0:-ord(date[-1])]

    def fill_method(self, aes_str):
        '''pkcs7补全'''
        pad_pkcs7 = pad(aes_str.encode('utf-8'), AES.block_size, style='pkcs7')

        return pad_pkcs7

    def encrypt(self, encrData, result="hex"):
        # 加密函数,使用pkcs7补全
        en_cryptor = AES.new(self.key.encode("utf-8"), AES.MODE_CBC, iv=self.iv.encode("utf-8"))
        res = en_cryptor.encrypt( self.fill_method(encrData))
        if result == "hex":
            msg = binascii.b2a_hex(res).decode()
        elif result == "jy3":
            msg = str(e1(res))
        else:
            # 转换为base64
            msg = str(base64.b64encode(res), encoding="utf-8")
        return msg


if __name__ == '__main__':
    import asyncio

    # r = Rsa()
    # print(r.Rencrypt('143.84615384615384'))
    c = Cbc("b054ef27070bb3ec", "0000000000000000")
    data = '{"lang":"en-NL","userresponse":"37bbb33a1f2","passtime":402,"imgload":146,"aa":"O--.,--a--@--J,(!!Os(t(()(((q((()ytyssssssssttts(!!(,111/112.111/11173A1L1J/999A$)G","ep":{"v":"7.9.2","$_BIE":false,"me":true,"tm":{"a":1735113631870,"b":1735113632089,"c":1735113632089,"d":0,"e":0,"f":1735113631877,"g":1735113631877,"h":1735113631877,"i":1735113631877,"j":1735113631877,"k":0,"l":1735113631907,"m":1735113632085,"n":1735113632102,"o":1735113632097,"p":1735113632618,"q":1735113633806,"r":1735113633807,"s":1735113640697,"t":1735113640697,"u":1735113640707},"td":-1},"h9s9":"1816378497","rp":"0f7b57cc73dd1851cec1d48d343d5ba2"}'
    a = asyncio.run(c.encrypt(data, result="jy3"))
    print(a)
