# coding: utf-8

import hashlib
from Crypto.Cipher import AES
import base64
import urllib


def pp(string):
    print("%s\n" % (string,))
def encipher_value(password, padding="{", secret=""):
    block_size = 32
    secretMd5 = hashlib.md5(secret).hexdigest()
    pp(secretMd5)
    pad = lambda s: s + (block_size - len(s) % block_size) * padding
    password_pad = pad(password)
    pp(password_pad)
    cipher = AES.new(secretMd5.encode(encoding="utf-8"), mode=AES.MODE_ECB)
    aesEncrypt = cipher.encrypt(password_pad.encode(encoding="utf-8"))
    pp(aesEncrypt)
    base64Encode = base64.b64encode(aesEncrypt)
    pp(base64Encode)
    urlEncode = urllib.quote(base64Encode, safe="")
    return urlEncode

pp(encipher_value('test_password',secret='test_secret'))